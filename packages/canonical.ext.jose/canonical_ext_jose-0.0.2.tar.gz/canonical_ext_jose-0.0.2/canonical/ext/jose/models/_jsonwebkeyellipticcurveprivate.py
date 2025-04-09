import pydantic
from cryptography.hazmat.primitives.asymmetric.ec import generate_private_key
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateNumbers
from libcanonical.types import AwaitableBytes
from libcanonical.utils.encoding import b64encode_int
from libcanonical.utils.encoding import b64decode_int

from canonical.ext.jose.types import JSONWebAlgorithm
from canonical.ext.jose.utils import normalize_ec_signature
from ._jsonwebkeyellipticcurvepublic import JSONWebKeyEllipticCurvePublic


class JSONWebKeyEllipticCurvePrivate(JSONWebKeyEllipticCurvePublic):
    model_config = {'extra': 'forbid'}

    d: str = pydantic.Field(
        default=...,
        title="ECC private key",
        description=(
            "The `d` (ECC private key) parameter contains the elliptic "
            "curve private key value. It is represented as the base64url "
            "encoding of the octet string representation of the private "
            "key value, as defined in Section 2.3.7 of SEC1. The length "
            "of this octet string MUST be ceiling(log-base-2(n)/8) octets "
            "(where n is the order of the curve)."
        )
    )

    @property
    def private_numbers(self):
        return EllipticCurvePrivateNumbers(
            public_numbers=self.public_numbers,
            private_value=b64decode_int(self.d)
        )

    @property
    def private_key(self):
        return self.private_numbers.private_key()

    @classmethod
    def generate(
        cls,
        alg: JSONWebAlgorithm,
    ) -> 'JSONWebKeyEllipticCurvePrivate':
        if alg.config.crv is None:
            raise ValueError(f"Not an elliptic curve algorithm: {alg}")
        k = generate_private_key(cls.get_curve(alg.config.crv))
        n = k.private_numbers()
        return cls.model_validate({
            **alg.config.params(),
            'd': b64encode_int(n.private_value),
            'x': b64encode_int(n.public_numbers.x),
            'y': b64encode_int(n.public_numbers.y)
        })

    def get_public_key(self):
        return JSONWebKeyEllipticCurvePublic.model_validate({
            **self.model_dump(
                exclude={'d'}
            ),
            'key_ops': (self.key_ops & {'verify', 'encrypt', 'wrapKey'}) if self.key_ops else None
        })

    def sign(self, message: bytes, alg: JSONWebAlgorithm | None = None) -> AwaitableBytes:
        alg = alg or self.alg
        if alg is None:
            raise ValueError(f"The `alg` parameter is required.")
        sig = normalize_ec_signature(
            l=(self.public_key.curve.key_size + 7) // 8,
            sig=self.private_key.sign(message, ECDSA(self.get_hash(alg)))
        )
        return AwaitableBytes(sig)