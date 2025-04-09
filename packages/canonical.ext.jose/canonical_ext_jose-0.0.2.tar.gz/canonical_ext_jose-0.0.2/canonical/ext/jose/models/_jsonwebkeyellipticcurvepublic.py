from typing import ClassVar
from typing import Literal

import pydantic
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicNumbers
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurve
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA
from cryptography.hazmat.primitives.asymmetric.ec import SECP256K1
from cryptography.hazmat.primitives.asymmetric.ec import SECP256R1
from cryptography.hazmat.primitives.asymmetric.ec import SECP384R1
from cryptography.hazmat.primitives.asymmetric.ec import SECP521R1
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from libcanonical.types import AwaitableBool
from libcanonical.utils.encoding import b64decode_int
from libcanonical.utils.encoding import bytes_to_number

from canonical.ext.jose.types import JSONWebAlgorithm
from ._jsonwebkeybase import JSONWebKeyBase


class JSONWebKeyEllipticCurvePublic(JSONWebKeyBase[
    Literal['EC'],
    Literal['sign', 'verify', 'encrypt', 'decrypt']
]):
    model_config = {'extra': 'forbid'}
    thumbprint_claims = ["crv", "kty", "x", "y"]
    curves: ClassVar[dict[str, type[EllipticCurve]]] = {
        'P-256': SECP256R1,
        'P-256K': SECP256K1,
        'P-384': SECP384R1,
        'P-521': SECP521R1,
    }

    crv: Literal['P-256', 'P-256K', 'P-384', 'P-521'] = pydantic.Field(
        default=...,
        title="Curve",
        description=(
            "The `crv` (curve) parameter identifies the "
            "cryptographic curve used with the key."
        )
    )

    x: str = pydantic.Field(
        default=...,
        title="X coordinate",
        description=(
            "The `x` (x coordinate) parameter contains the x "
            "coordinate for the Elliptic Curve point. It is "
            "represented as the base64url encoding of the octet "
            "string representation of the coordinate, as defined "
            "in Section 2.3.5 of SEC1. The length of this octet "
            "string MUST be the full size of a coordinate for "
            "the curve specified in the `crv` parameter. For "
            "example, if the value of `crv` is `P-521`, the octet "
            "string must be 66 octets long."
        )
    )

    y: str = pydantic.Field(
        default=...,
        title="Y coordinate",
        description=(
            "The `y` (y coordinate) parameter contains the y "
            "coordinate for the Elliptic Curve point. It is "
            "represented as the base64url encoding of the octet "
            "string representation of the coordinate, as defined "
            "in Section 2.3.5 of SEC1. The length of this octet "
            "string MUST be the full size of a coordinate for "
            "the curve specified in the `crv` parameter. For "
            "example, if the value of `crv` is `P-521`, the "
            "octet string must be 66 octets long."
        )
    )

    @property
    def public_numbers(self) -> EllipticCurvePublicNumbers:
        return EllipticCurvePublicNumbers(
            curve=self.get_curve(self.crv),
            x=b64decode_int(self.x),
            y=b64decode_int(self.y)
        )

    @property
    def public_key(self):
        return self.public_numbers.public_key()

    @classmethod
    def get_curve(cls, crv: str):
        return cls.curves[crv]()

    @classmethod
    def supports_algorithm(cls, alg: JSONWebAlgorithm) -> bool:
        return alg.config.kty == 'EC'

    def get_public_key(self):
        return JSONWebKeyEllipticCurvePublic.model_validate(self.model_dump())

    def is_asymmetric(self) -> bool:
        return True

    def verify(
        self,
        signature: bytes,
        message: bytes,
        alg: JSONWebAlgorithm
    ) -> AwaitableBool:
        n = (self.public_key.curve.key_size + 7) // 8
        try:
            self.public_key.verify(
                signature=encode_dss_signature(
                    bytes_to_number(signature[:n]),
                    bytes_to_number(signature[n:]),
                ),
                data=message,
                signature_algorithm=ECDSA(self.get_hash(alg))
            )
            return AwaitableBool(True)
        except InvalidSignature:
            return AwaitableBool(False)