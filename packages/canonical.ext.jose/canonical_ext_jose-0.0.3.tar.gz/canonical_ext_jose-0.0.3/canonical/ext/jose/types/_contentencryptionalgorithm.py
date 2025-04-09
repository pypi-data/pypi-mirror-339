import os
from typing import ClassVar
from typing import Literal

from libcanonical.types import StringType

from ._contentencryptionkey import ContentEncryptionKey
from ._contentencryptionalgorithmconfig import ContentEncryptionAlgorithmConfig


class ContentEncryptionAlgorithm(StringType):
    config: ContentEncryptionAlgorithmConfig
    registry: ClassVar[dict[str, ContentEncryptionAlgorithmConfig]] = {}

    @classmethod
    def register(
        cls,
        name: str,
        l: int,
        cipher: Literal['AES'],
        mode: Literal['CBC', 'GCM']
    ):
        cls.registry[name] = ContentEncryptionAlgorithmConfig(
            name=name,
            bits=l,
            cipher=cipher,
            mode=mode
        )

    def generate(self) -> ContentEncryptionKey:
        return ContentEncryptionKey(self.config, os.urandom(self.config.bits // 8))

    def __new__(cls, object: object):
        self = super().__new__(cls, object)
        try:
            self.config = ContentEncryptionAlgorithm.registry[self]
        except KeyError:
            raise ValueError(f"Unsupported content encryption algorithm: {self}")
        return self


ContentEncryptionAlgorithm.register('A128GCM', l=128, cipher='AES', mode='GCM')
ContentEncryptionAlgorithm.register('A192GCM', l=192, cipher='AES', mode='GCM')
ContentEncryptionAlgorithm.register('A256GCM', l=256, cipher='AES', mode='GCM')