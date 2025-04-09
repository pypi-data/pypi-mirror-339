from typing import Literal

import pydantic
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from libcanonical.types import AwaitableBool
from libcanonical.types import Base64

from canonical.ext.jose.types import JSONWebAlgorithm
from ._jsonwebkeybase import JSONWebKeyBase


class JSONWebKeyEdwardsCurvePublic(JSONWebKeyBase[
    Literal['OKP'],
    Literal['sign', 'verify', 'encrypt', 'decrypt']
]):
    model_config = {'extra': 'forbid'}

    crv: Literal['Ed25519', 'X25519'] = pydantic.Field(
        default=...,
        title="Curve",
        description=(
            "The `crv` (curve) parameter identifies the "
            "cryptographic curve used with the key."
        )
    )

    x: Base64 = pydantic.Field(
        default=...,
        title="Public key",
        description=(
            "Contains the public key encoded using the base64url encoding."
        )
    )

    @property
    def public_key(self):
        return Ed25519PublicKey.from_public_bytes(self.x)

    def is_asymmetric(self) -> bool:
        return True

    def verify(
        self,
        signature: bytes,
        message: bytes,
        alg: JSONWebAlgorithm
    ) -> AwaitableBool:
        try:
            self.public_key.verify(signature, message)
            return AwaitableBool(True)
        except InvalidSignature:
            return AwaitableBool(False)