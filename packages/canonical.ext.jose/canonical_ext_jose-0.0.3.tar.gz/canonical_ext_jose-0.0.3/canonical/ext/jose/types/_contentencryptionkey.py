import os
from typing import TYPE_CHECKING

from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import GCM
from libcanonical.types import AwaitableBytes

from ._encryptionresult import EncryptionResult
if TYPE_CHECKING:
    from ._contentencryptionalgorithmconfig import ContentEncryptionAlgorithmConfig


class ContentEncryptionKey:

    def __init__(
        self,
        config: 'ContentEncryptionAlgorithmConfig',
        k: bytes
    ):
        self.config = config
        self.k = k

    def decrypt(self, result: EncryptionResult):
        match self.config.mode:
            case 'GCM':
                return self.decrypt_aes_gcm_aead(result)
            case _:
                raise NotImplementedError(self.config.mode)

    def decrypt_aes_gcm_aead(self, result: EncryptionResult):
        decryptor = Cipher(
            AES(self.k),
            GCM(result.iv, result.tag),
        ).decryptor()
        decryptor.authenticate_additional_data(result.aad)
        return AwaitableBytes(decryptor.update(result.ct) + decryptor.finalize())

    def encrypt(self, pt: bytes, aad: bytes = b'') -> EncryptionResult:
        match self.config.mode:
            case 'GCM':
                # AES-GCM with AAD.
                return self.encrypt_aes_aead(pt, aad)
            case _:
                raise NotImplementedError(self.config.mode)

    def encrypt_aes_aead(self, pt: bytes, aad: bytes) -> EncryptionResult:
        # Use of an IV of size 96 bits is REQUIRED with this algorithm.
        iv = os.urandom(12)
        enc = Cipher(AES(self.k), GCM(iv)).encryptor()
        enc.authenticate_additional_data(aad)
        ct = enc.update(pt) + enc.finalize()
        return EncryptionResult(
            ct=ct,
            iv=iv,
            tag=enc.tag
        )

    def __bytes__(self):
        return self.k
