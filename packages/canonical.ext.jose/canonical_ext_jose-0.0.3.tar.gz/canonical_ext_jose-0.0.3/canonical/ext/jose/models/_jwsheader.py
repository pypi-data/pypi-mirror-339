import pydantic
from libcanonical.types import Base64
from libcanonical.types import Base64URLEncoded
from libcanonical.types import HTTPResourceLocator
from libcanonical.utils.encoding import b64decode_json
from libcanonical.utils.encoding import b64encode

from canonical.ext.jose.types import JSONWebAlgorithm
from ._jsonwebkey import JSONWebKey


class JWSHeader(pydantic.BaseModel):
    model_config = {'extra': 'forbid'}

    alg: JSONWebAlgorithm = pydantic.Field(
        default=...
    )

    jku: HTTPResourceLocator | None = pydantic.Field(
        default=None
    )

    jwk: JSONWebKey | None = pydantic.Field(
        default=None
    )

    kid: str | None = pydantic.Field(
        default=None
    )

    x5u: HTTPResourceLocator | None = pydantic.Field(
        default=None
    )

    x5c: list[Base64] | None = pydantic.Field(
        default=None
    )

    x5t: Base64URLEncoded | None = pydantic.Field(
        default=None
    )

    x5t_s256: Base64URLEncoded | None = pydantic.Field(
        default=None,
        alias='x5t#S256'
    )

    typ: str | None = pydantic.Field(
        default=None
    )

    cty: str | None = pydantic.Field(
        default=None
    )

    crit: list[str] | None = pydantic.Field(
        default=None
    )

    @classmethod
    def model_validate_b64(cls, buf: bytes):
        return cls.model_validate(b64decode_json(buf))

    def __str__(self):
        return self.model_dump_json(
            exclude_none=True,
            by_alias=True
        )

    def __bytes__(self):
        return Base64(str.encode(str(self), 'utf-8'))

    async def sign(self, signer: JSONWebKey, payload: bytes):
        message = bytes.join(b'.', [
            b64encode(bytes(self)),
            payload
        ])
        return Base64(signer.sign(message, alg=self.alg))