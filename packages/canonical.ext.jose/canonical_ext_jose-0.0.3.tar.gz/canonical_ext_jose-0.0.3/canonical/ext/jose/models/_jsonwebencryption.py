from typing import Any
from typing import Union

import pydantic
from libcanonical.types import Base64
from libcanonical.utils.encoding import b64encode_json

from canonical.ext.jose.types import ContentEncryptionKey
from canonical.ext.jose.types import ContentEncryptionAlgorithm
from canonical.ext.jose.types import JSONWebAlgorithm
from canonical.ext.jose.types import JWECompactEncoded
from ._jsonwebkey import JSONWebKey
from ._jweheader import JWEHeader
from ._jwegeneralserialization import JWEGeneralSerialization
from ._recipient import Recipient



JSONWebEncryptionType = Union[
    JWECompactEncoded,
    JWEGeneralSerialization
]


class JSONWebEncryption(pydantic.RootModel[JSONWebEncryptionType]):

    @classmethod
    async def create(
        cls,
        *,
        key: JSONWebKey,
        alg: JSONWebAlgorithm,
        payload: bytes,
        enc: ContentEncryptionAlgorithm | None = None,
        protected: dict[str, Any] | None = None,
        unprotected: dict[str, Any] | None = None,
    ):
        header = JWEHeader(alg=alg, enc=enc)

        # If the algorithm needs a content encryption key, then
        # the `enc` parameter must specify its algorithm.
        if not alg.wraps() and enc is None:
            raise TypeError(
                "The `enc` parameter is required when using wrapping "
                "algorithms."
            )
        match alg.config.mode:
            case 'KEY_ENCRYPTION':
                assert enc is not None
                cek = enc.generate()
                encrypted_key = await key.encrypt(bytes(cek))
            case 'KEY_AGREEMENT_WITH_KEY_WRAPPING':
                assert enc is not None
                cek = enc.generate()
                encrypted_key = await key.encrypt(bytes(cek))
            case 'KEY_WRAPPING':
                assert enc is not None
                cek = enc.generate()
                encrypted_key = await key.encrypt(bytes(cek))

            # When Direct Key Agreement or Direct Encryption are employed,
            # #let the JWE Encrypted Key be the empty octet sequence.
            case 'DIRECT_ENCRYPTION':
                encrypted_key = b''
                raise NotImplementedError
            case 'DIRECT_KEY_AGREEMENT':
                encrypted_key = b''
                raise NotImplementedError
            case _:
                raise ValueError(f"Not an encryption algorithm: {alg}")

        aad = b''
        if protected:
            aad = b64encode_json(protected)
        if encrypted_key:
            encrypted_key.add_to_header(header)

        result = await cek.encrypt(payload, aad)
        jwe = cls.model_validate({
            'ciphertext': Base64(result),
            'iv': Base64(result.iv),
            'tag': Base64(result.tag),
            'recipients': [
                Recipient(
                    header=header.model_dump(),
                    encrypted_key=Base64(encrypted_key)
                )
            ]
        })
        jwe.set_content_encryption_key(cek)
        return jwe

    def model_post_init(self, _: Any) -> None:
        if isinstance(self.root, JWECompactEncoded):
            self.root = self.root.jose(JWEGeneralSerialization)

    def decrypt(self, key: JSONWebKey):
        assert isinstance(self.root, JWEGeneralSerialization)
        return self.root.decrypt(key)

    def set_content_encryption_key(
        self,
        cek: ContentEncryptionKey | JSONWebKey
    ):
        assert isinstance(self.root, JWEGeneralSerialization)
        self.root.set_content_encryption_key(cek)