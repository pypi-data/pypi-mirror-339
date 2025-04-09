import pydantic
from libcanonical.types import Base64

from canonical.ext.jose.types import ContentEncryptionKey
from canonical.ext.jose.types import EncryptionResult
from ._jsonwebkey import JSONWebKey
from ._jweheader import JWEHeader


class Recipient(pydantic.BaseModel):
    header: JWEHeader = pydantic.Field(
        default=JWEHeader(),
        title="Header",
        description=(
            "The `header` member MUST be present and contain the value JWE Per-"
            "Recipient Unprotected Header when the JWE Per-Recipient Unprotected "
            "Header value is non-empty; otherwise, it MUST be absent.  This "
            "value is represented as an unencoded JSON object, rather than as "
            "a string.  These Header Parameter values are not integrity protected."
        )
    )

    encrypted_key: Base64 = pydantic.Field(
        default_factory=Base64,
        title="Encrypted key",
        description=(
            "The `encrypted_key` member MUST be present and contain the value "
            "`BASE64URL(JWE Encrypted Key)` when the JWE Encrypted Key value "
            "is non-empty; otherwise, it MUST be absent."
        )
    )

    @property
    def ct(self):
        return EncryptionResult(
            ct=self.encrypted_key,
        )

    def might_decrypt(self, key: JSONWebKey, header: JWEHeader):
        """Return a boolean indicating if the given :class:`JSONWebKey` `key`
        _might_ decrypt the encrypted key.
        """
        if not self.encrypted_key:
            raise NotImplementedError
        return any([
            key.kid and key.kid == header.kid,
            header.jwk and header.jwk.thumbprint('sha256') == key.thumbprint('sha256'),
            key.alg and key.alg == (self.header.alg or header.alg)
        ])

    async def decrypt(self, key: JSONWebKey, header: JWEHeader):
        if not self.encrypted_key:
            raise ValueError(
                "Recipient does not have an ecnryption key."
            )
        enc = header.enc or self.header.enc
        if enc is None:
            raise ValueError("Unable to determine encryption algorithm.")
        return ContentEncryptionKey(enc.config, k=await key.decrypt(self.ct))