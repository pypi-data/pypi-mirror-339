import functools
from typing import Any

import pydantic
from libcanonical.types import Base64

from canonical.ext.jose.types import ContentEncryptionKey
from canonical.ext.jose.types import EncryptionResult
from ._jsonwebkey import JSONWebKey
from ._jweheader import JWEHeader
from ._recipient import Recipient


class JWEGeneralSerialization(pydantic.BaseModel):
    protected: Base64 = pydantic.Field(
        default_factory=Base64,
        title="Protected",
        description=(
            "The `protected` member MUST be present and contain "
            "the value `BASE64URL(UTF8(JWE Protected Header))` "
            "when the JWE Protected Header value is non-empty; "
            "otherwise, it MUST be absent. These Header Parameter "
            "values are integrity protected."
        )
    )

    unprotected: dict[str, Any] = pydantic.Field(
        default_factory=dict,
        title="Header",
        description=(
            "The `unprotected` member MUST be present and contain "
            "the value JWE Shared Unprotected Header when the JWE "
            "Shared Unprotected Header value is non-empty; otherwise, "
            "it MUST be absent.  This value is represented as an "
            "unencoded JSON object, rather than as a string. These "
            "Header Parameter values are not integrity protected."
        )
    )

    iv: Base64 = pydantic.Field(
        default_factory=Base64,
        title="Initialization Vector (IV)",
        description=(
            "The `iv` member MUST be present and contain the value "
            "`BASE64URL(JWE Initialization Vector)` when the JWE "
            "Initialization Vector value is non-empty; otherwise, "
            "it MUST be absent."
        )
    )

    aad: Base64 = pydantic.Field(
        default_factory=Base64,
        title="Additional Authenticated Data (AAD)",
        description=(
            "The `aad` member MUST be present and contain the value "
            "`BASE64URL(JWE AAD))` when the JWE AAD value is non-empty; "
            "otherwise, it MUST be absent.  A JWE AAD value can be "
            "included to supply a base64url-encoded value to be integrity "
            "protected but not encrypted."
        )
    )

    ciphertext: Base64 = pydantic.Field(
        default=...,
        title="Ciphertext",
        description=(
            "The `ciphertext` member MUST be present and "
            "contain the value `BASE64URL(JWE Ciphertext)`."
        )
    )

    tag: Base64 = pydantic.Field(
        default_factory=Base64,
        title="Tag",
        description=(
            "The `tag` member MUST be present and contain the "
            "value `BASE64URL(JWE Authentication Tag)` when the "
            "JWE Authentication Tag value is non-empty; otherwise, "
            "it MUST be absent."
        )
    )

    recipients: list[Recipient] = pydantic.Field(
        default_factory=list,
        title="Recipients",
        description=(
            "The `recipients` member value MUST be an array of JSON objects. "
            "Each object contains information specific to a single recipient. "
            "This member MUST be present with exactly one array element per "
            "recipient, even if some or all of the array element values are the "
            "empty JSON object `{}` (which can happen when all Header Parameter "
            "values are shared between all recipients and when no encrypted key "
            "is used, such as when doing Direct Encryption)"
        )
    )

    _cek: JSONWebKey | ContentEncryptionKey | None = pydantic.PrivateAttr(
        default=None
    )

    @functools.cached_property
    def encryption_result(self):
        return EncryptionResult(
            iv=self.iv,
            ct=self.ciphertext,
            tag=self.tag,
            aad=self.protected.urlencode()
        )

    @functools.cached_property
    def header(self) -> JWEHeader:
        return JWEHeader.model_validate({
            **self.unprotected,
            **JWEHeader.model_validate_json(self.protected).model_dump()
        })

    @pydantic.model_validator(mode='after')
    def validate_rfc7516(self):
        # The Header Parameter values used when creating or validating per-
        # recipient ciphertext and Authentication Tag values are the union of
        # the three sets of Header Parameter values that may be present: (1)
        # the JWE Protected Header represented in the "protected" member, (2)
        # the JWE Shared Unprotected Header represented in the "unprotected"
        # member, and (3) the JWE Per-Recipient Unprotected Header represented
        # in the "header" member of the recipient's array element.  The union
        # of these sets of Header Parameters comprises the JOSE Header.  The
        # Header Parameter names in the three locations MUST be disjoint.
        claims: set[str] = set(self.unprotected.keys())
        if self.protected:
            protected = JWEHeader.model_validate_json(self.protected)
            protected_claims = set(protected.model_dump(exclude_defaults=True))
            unprotected_claims = set(self.unprotected.keys())
            conflicting = protected_claims & unprotected_claims
            if conflicting:
                raise ValueError(
                    "The header parameters in the protected and unprotected "
                    "header must be disjoint."
                )
            claims.update(protected_claims)
        for recipient in self.recipients:
            if not bool(claims & set(recipient.header.keys())):
                continue
            raise ValueError(
                "The header parameters in the protected, unprotected "
                "and recipient header must be disjoint."
            )
        return self

    def set_content_encryption_key(
        self,
        cek: ContentEncryptionKey | JSONWebKey
    ):
        if self._cek is not None:
            raise ValueError(
                "A Content Encryption Key (CEK) is already supplied."
            )
        self._cek = cek

    async def decrypt(self, key: JSONWebKey) -> bytes:
        if not self._cek:
            self._cek = await self.decrypt_cek(key)
        return await self._cek.decrypt(self.encryption_result)

    async def decrypt_cek(self, key: JSONWebKey):
        candidates: list[Recipient] = []
        for recipient in self.recipients:
            if not recipient.might_decrypt(key, self.header):
                continue
            candidates.append(recipient)
        if len(candidates) > 1:
            raise NotImplementedError
        if len(candidates) == 0:
            raise NotImplementedError
        print(repr(self.encryption_result.tag), repr(self.encryption_result.aad))
        return await candidates[0].decrypt(key, self.header)