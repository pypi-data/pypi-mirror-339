import json

import pydantic
from libcanonical.utils.encoding import b64encode

from canonical.ext.jose.types import JSONWebAlgorithm
from canonical.ext.jose.types import ContentEncryptionAlgorithm
from ._jsonwebkey import JSONWebKey


class JWEHeader(pydantic.BaseModel):
    alg: JSONWebAlgorithm | None = pydantic.Field(
        default=None
    )

    enc: ContentEncryptionAlgorithm | None = pydantic.Field(
        default=None
    )

    kid: str | None = pydantic.Field(
        default=None
    )

    jwk: JSONWebKey | None = pydantic.Field(
        default=None
    )

    def keys(self):
        return set(self.model_dump(exclude_defaults=True))

    def urlencode(self):
        claims = self.model_dump(
            exclude_defaults=True,
            exclude_none=True,
            mode='json'
        )

        # Compute the Encoded Protected Header value BASE64URL(UTF8(JWE Protected Header)).
        # If the JWE Protected Header is not present (which can only happen when using
        # the JWE JSON Serialization and no "protected" member is present), let this value
        # be the empty string.
        encoded = b''
        if claims:
            encoded = b64encode(
                json.dumps(encoded),
                encoder=bytes
            )
        return encoded