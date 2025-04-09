import os
from typing import ClassVar
from typing import Literal

import pydantic
from cryptography.hazmat.primitives.keywrap import aes_key_unwrap
from libcanonical.types import AwaitableBytes
from libcanonical.types import Base64

from canonical.ext.jose.types import EncryptionResult
from canonical.ext.jose.types import JSONWebAlgorithm
from ._jsonwebkeybase import JSONWebKeyBase


class SymmetricEncryptionKey(
    JSONWebKeyBase[
        Literal['oct'],
        Literal['encrypt', 'decrypt', 'unwrapKey', 'wrapKey'],
        Literal['enc']
    ]
):
    crv: ClassVar[None] = None
    thumbprint_claims = ['k', 'kty']

    k: Base64 = pydantic.Field(
        default=...,
        title="Key",
        description=(
            "The `k` (key value) parameter contains the value of the symmetric (or "
            "other single-valued) key. It is represented as the base64url encoding "
            "of the octet sequence containing the key value."
        )
    )

    @classmethod
    def generate(cls, alg: JSONWebAlgorithm, length: int | None = None):
        length = alg.config.length or length
        if length is None:
            raise TypeError(
                f"The length could not be determined from algorithm {alg} "
                "and the `length` paramter was None."
            )
        return cls.model_validate({
            **alg.config.params(),
            'k': Base64(os.urandom(length // 8))
        })

    def decrypt(self, result: EncryptionResult) -> AwaitableBytes:
        if self.alg is None:
            raise NotImplementedError
        match self.alg.config.mode:
            case 'KEY_WRAPPING':
                return self.unwrap(result)
            case _:
                raise NotImplementedError(f"Unsupported decryption mode: {self.alg.config.mode}")

    def unwrap(self, result: EncryptionResult):
        return AwaitableBytes(aes_key_unwrap(self.k, result.ct))