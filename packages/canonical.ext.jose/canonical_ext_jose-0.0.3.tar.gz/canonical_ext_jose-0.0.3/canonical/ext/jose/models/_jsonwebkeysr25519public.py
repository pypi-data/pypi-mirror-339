from typing import Literal

import pydantic
from libcanonical.types import Base64

from ._jsonwebkeybase import JSONWebKeyBase


class JSONWebKeySR25519Public(JSONWebKeyBase[
    Literal['OKP'],
    Literal['sign', 'verify']
]):
    model_config = {'extra': 'forbid'}
    thumbprint_claims = ["crv", "kty", "x"]

    crv: Literal['Sr25519'] = pydantic.Field(
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
        max_length=32,
        min_length=32,
        description=(
            "Contains the public key encoded using the base64url encoding."
        )
    )

    def is_asymmetric(self) -> bool:
        return True