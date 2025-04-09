import time
from typing import overload
from typing import Any
from typing import Literal
from typing import Union

import pydantic
from libcanonical.types import AwaitableBytes

from canonical.ext.jose.types import EncryptionResult
from canonical.ext.jose.types import JSONWebAlgorithm
from canonical.ext.jose.types import ThumbprintHashAlgorithm
from ._jsonwebkeyedwardscurveprivate import JSONWebKeyEdwardsCurvePrivate
from ._jsonwebkeyedwardscurvepublic import JSONWebKeyEdwardsCurvePublic
from ._jsonwebkeyellipticcurveprivate import JSONWebKeyEllipticCurvePrivate
from ._jsonwebkeyellipticcurveprivate import JSONWebKeyEllipticCurvePublic
from ._jsonwebkeyrsaprivate import JSONKeyRSAPrivate
from ._jsonwebkeyrsapublic import JSONKeyRSAPublic
from ._jsonwebkeysr25519private import JSONWebKeySR25519Private
from ._jsonwebkeysr25519public import JSONWebKeySR25519Public
from ._symmetricencryptionkey import SymmetricEncryptionKey


__all__: list[str] = [
    'JSONWebKey'
]


JSONWebKeyType = Union[
    JSONWebKeyEdwardsCurvePrivate,
    JSONWebKeyEllipticCurvePrivate,
    JSONKeyRSAPrivate,
    JSONWebKeySR25519Private,
    JSONWebKeyEdwardsCurvePublic,
    JSONWebKeyEllipticCurvePublic,
    JSONKeyRSAPublic,
    JSONWebKeySR25519Public,
    SymmetricEncryptionKey
]


class JSONWebKey(pydantic.RootModel[JSONWebKeyType]):

    @property
    def alg(self): # pragma: no cover
        return self.root.alg

    @property
    def crv(self): # pragma: no cover
        return self.root.crv

    @property
    def kid(self) -> str | None: # pragma: no cover
        return self.root.kid

    @property
    def key_ops(self): # pragma: no cover
        return self.root.key_ops

    @property
    def kty(self): # pragma: no cover
        return self.root.kty

    @property
    def public(self) -> Union['JSONWebKey', None]: # pragma: no cover
        key = None
        if self.is_asymmetric():
            key = JSONWebKey(root=self.root.public)
        return key

    @property
    def use(self): # pragma: no cover
        return self.root.use

    @overload
    @classmethod
    def generate(
        cls,
        alg: JSONWebAlgorithm | str,
        **kwargs: Any
    ) -> 'JSONWebKey':  # pragma: no cover
        ...

    @overload
    @classmethod
    def generate(
        cls,
        kty: Literal['RSA'],
        length: int = 4096,
        exponent: int = 65537,
        **kwargs: Any
    ) -> 'JSONWebKey': # pragma: no cover
        ...

    @overload
    @classmethod
    def generate(
        cls,
        alg: Literal['EdDSA'],
        crv: Literal['Ed448', 'Ed25519'],
        **kwargs: Any
    ) -> 'JSONWebKey': # pragma: no cover
        ...

    @overload
    @classmethod
    def generate(
        cls,
        kty: Literal['EC'],
        crv: str,
        *kwargs: Any
    ) -> 'JSONWebKey': # pragma: no cover
        ...

    @classmethod
    def generate(  # type: ignore
        cls,
        kty: Literal['RSA', 'EC', 'OKP', 'oct'] | None = None,
        alg: JSONWebAlgorithm | str | None = None,
        kid: str | None = None,
        **kwargs: Any
    ):
        if not kty and not alg: # pragma: no cover
            raise ValueError("Either the `kty` or `alg` parameter must be specified.")
        if isinstance(alg, str):
            alg = JSONWebAlgorithm.validate(alg)
        root: JSONWebKeyType | None = None
        if alg is not None:
            kwargs['alg'] = alg
            kty = alg.config.kty
        assert alg is not None
        match kty:
            case 'RSA':
                root = JSONKeyRSAPrivate.generate(**kwargs)
            case 'EC':
                root = JSONWebKeyEllipticCurvePrivate.generate(**kwargs)
            case 'OKP':
                assert alg is not None
                match alg.config.crv:
                    case 'Sr25519':
                        root = JSONWebKeySR25519Private.generate(alg)
                    case _: # pragma: no cover
                        root = JSONWebKeyEdwardsCurvePrivate.generate(alg)
            case 'oct':
                match alg.config.use:
                    case 'enc':
                        root = SymmetricEncryptionKey.generate(alg)
                    case 'sig':
                        raise NotImplementedError
            case _: # pragma: no cover
                raise ValueError(f"Unsupported algorithm: {alg}")
        assert root is not None
        root.iat = int(time.time())
        root.kid = kid
        return cls(root=root)

    def can_verify(self, alg: JSONWebAlgorithm | None):
        """Return a boolean indicating if the key can verify a signature
        with the specified parameters.
        """
        return all([
            self.use in {None, 'sig'},
            not self.key_ops or ('verify' in self.key_ops),
            alg is None or self.root.supports_algorithm(alg)
        ])

    def is_asymmetric(self): # pragma: no cover
        return self.root.is_asymmetric()

    def is_public(self): # pragma: no cover
        return type(self.root) in (
            JSONWebKeyEllipticCurvePublic,
            JSONKeyRSAPublic,
            JSONWebKeySR25519Public,
        )

    def json(self): # type: ignore
        return self.model_dump_json( # pragma: no cover
            exclude_defaults=True
        )

    def decrypt(self, result: EncryptionResult):
        return self.root.decrypt(result)

    def encrypt(
        self,
        pt: bytes,
        aad: bytes | None = None,
        alg: JSONWebAlgorithm | None = None
    ) -> EncryptionResult:
        alg = alg or self.alg
        if alg is None:
            raise ValueError("Unable to select encryption algorithm.")
        if not self.root.supports_algorithm(alg):
            raise ValueError(f"Unsupported algorithm: {alg}")
        return self.root.encrypt(pt, aad, alg)

    def sign(self, message: bytes, alg: JSONWebAlgorithm | None = None) -> AwaitableBytes:
        return self.root.sign(message, alg=alg) # type: ignore

    def thumbprint(self, using: ThumbprintHashAlgorithm):
        return self.root.thumbprint(using=using)

    def verify(self, signature: bytes, message: bytes, alg: Any):
        return self.root.verify(signature, message, alg)

    def __str__(self):
        return self.root.model_dump_json(
            by_alias=True,
            exclude_none=True
        )