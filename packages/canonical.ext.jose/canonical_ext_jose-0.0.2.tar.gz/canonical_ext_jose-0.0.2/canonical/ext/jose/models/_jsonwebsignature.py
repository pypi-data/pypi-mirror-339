from typing import Any
from typing import Callable
from typing import Self
from typing import TypeVar

import pydantic

from canonical.ext.jose.types import JSONWebAlgorithm
from canonical.ext.jose.types import JWSCompactEncoded
from ._jsonwebkey import JSONWebKey
from ._signedjws import SignedJWS


T = TypeVar('T')


class JSONWebSignature(pydantic.RootModel[SignedJWS | JWSCompactEncoded]):

    @property
    def signatures(self):
        assert isinstance(self.root, SignedJWS)
        return tuple(self.root.signatures)

    @pydantic.field_serializer('root')
    def serialize_root(self, value: SignedJWS | JWSCompactEncoded):
        if isinstance(value, SignedJWS) and len(self.signatures) == 1:
            value = self.serialize()
        return value

    def serialize(self):
        buf = self.root
        if not isinstance(self.root, JWSCompactEncoded):
            buf = JWSCompactEncoded(self.root.serialize())
        return buf

    def deserialize(self, cls: Callable[[bytes], T] = bytes):
        """Deserializes the content of the JWS."""
        assert isinstance(self.root, SignedJWS)
        return self.root.deserialize(cls=cls)

    def model_dump(self, **kwargs: Any):
        kwargs.setdefault('exclude_defaults', True)
        kwargs.setdefault('exclude_none', True)
        return super().model_dump(**kwargs)

    def model_dump_json(self, **kwargs: Any):
        kwargs.setdefault('exclude_defaults', True)
        kwargs.setdefault('exclude_none', True)
        return super().model_dump_json(**kwargs)

    def model_post_init(self, _: Any) -> None:
        if isinstance(self.root, JWSCompactEncoded):
            self.root = SignedJWS.model_validate_compact(self.root) # type: ignore

    async def sign(
        self,
        signer: JSONWebKey,
        alg: JSONWebAlgorithm | None = None,
        kid: str | None = None,
        typ: str | None =None,
    ) -> Self:
        assert isinstance(self.root, SignedJWS)
        self.root = await self.root.sign(signer, alg, kid=kid, typ=typ)
        return self

    def verify(self, verifier: JSONWebKey):
        """Return a boolean indicating if at least one signature was valid."""
        assert isinstance(self.root, SignedJWS)
        return self.root.verify(verifier)