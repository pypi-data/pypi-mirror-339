import pydantic
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from libcanonical.types import AwaitableBytes
from libcanonical.types import Base64

from canonical.ext.jose.types import JSONWebAlgorithm
from ._jsonwebkeyedwardscurvepublic import JSONWebKeyEdwardsCurvePublic


class JSONWebKeyEdwardsCurvePrivate(JSONWebKeyEdwardsCurvePublic):
    model_config = {'extra': 'forbid'}

    d: Base64 = pydantic.Field(
        default=...,
        title="Private key",
        description=(
            "Contains the private key encoded using the base64url encoding. "
            "This parameter MUST NOT be present for public keys."
        )
    )

    @classmethod
    def generate(
        cls,
        alg: JSONWebAlgorithm | str
    ) -> 'JSONWebKeyEdwardsCurvePrivate':
        if not isinstance(alg, JSONWebAlgorithm):
            alg = JSONWebAlgorithm.validate(alg)
        if alg.config.crv not in {'Ed448', 'Ed25519'}:
            raise ValueError(f"Not an valid algorithm for {cls.__name__}: {alg}")
        k = Ed25519PrivateKey.generate()
        return cls.model_validate({
            **alg.config.params(),
            'x': Base64(k.public_key().public_bytes_raw()),
            'd': Base64(k.private_bytes_raw())
        })

    @classmethod
    def supports_algorithm(cls, alg: JSONWebAlgorithm) -> bool:
        return all([
            alg.config.kty == 'OKP',
            alg.config.crv in {'Ed448', 'Ed25519'}
        ])

    @property
    def private_key(self):
        return Ed25519PrivateKey.from_private_bytes(self.d)

    def sign(
        self,
        message: bytes,
        alg: JSONWebAlgorithm | None = None
    ) -> AwaitableBytes:
        return AwaitableBytes(self.private_key.sign(message))