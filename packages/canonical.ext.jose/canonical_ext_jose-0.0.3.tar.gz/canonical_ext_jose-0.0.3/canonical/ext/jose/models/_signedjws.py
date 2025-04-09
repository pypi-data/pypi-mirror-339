import asyncio
from typing import Callable
from typing import TypeVar
from typing import Generic
from typing import SupportsBytes

import pydantic
from libcanonical.types import Base64

from canonical.ext.jose.types import JSONWebAlgorithm
from ._jsonwebkey import JSONWebKey
from ._signature import Signature


T = TypeVar('T', bound=SupportsBytes, default=bytes)
P = TypeVar('P')


class SignedJWS(pydantic.BaseModel, Generic[T]):
    signatures: list[Signature] = pydantic.Field(
        default_factory=list
    )

    payload: bytes | T = pydantic.Field(
        default=...
    )

    @classmethod
    def model_validate_compact(cls, value: str):
        header, payload, signature = str.split(value, '.')
        return cls(
            signatures=[Signature.model_validate({'protected': header, 'signature': signature})],
            payload=str.encode(payload, 'ascii')
        )

    def deserialize(self, cls: Callable[[bytes], P]) -> P:
        assert isinstance(self.payload, bytes)
        return cls(Base64.b64decode(self.payload))

    def serialize(self, compact: bool = True):
        if compact and len(self.signatures) > 1:
            raise ValueError(
                "JWS Compact Serialization can not be used with multiple "
                "signatures."
            )
        match compact:
            case True:
                signature = self.signatures[0]
                if not signature.protected:
                    raise ValueError("Protected header is missing from the signature.")
                assert isinstance(signature.protected, Base64)
                assert isinstance(signature.signature, Base64)
                serialized = str.join('.', [
                    str(signature.protected),
                    bytes.decode(bytes(self.payload)),
                    str(signature.signature)
                ])
            case False:
                serialized = self.model_dump_json(
                    by_alias=True,
                    exclude_defaults=True
                )
        return serialized

    async def sign(
        self,
        signer: JSONWebKey,
        alg: JSONWebAlgorithm | None = None,
        kid: str | None = None,
        typ: str | None =None,
    ) -> 'SignedJWS[T]':
        alg = alg or signer.alg
        if alg is None:
            raise TypeError("The `alg` parameter can not be None.")
        sig = await Signature.create(
            signer,
            alg=alg,
            payload=bytes(self.payload),
            kid=kid,
            typ=typ,
        )
        self.signatures.append(sig)
        return self

    async def verify(self, verifier: JSONWebKey) -> bool:
        if not any([verifier.can_verify(sig.alg) for sig in self.signatures]):
            return False
        assert isinstance(self.payload, bytes)
        return any(await asyncio.gather(*[
            sig.verify(verifier, self.payload)
            for sig in self.signatures
        ]))