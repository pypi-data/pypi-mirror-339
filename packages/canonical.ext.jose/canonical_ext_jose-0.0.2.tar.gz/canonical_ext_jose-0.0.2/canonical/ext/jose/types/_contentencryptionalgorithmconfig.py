from typing import Literal


class ContentEncryptionAlgorithmConfig:
    cipher: Literal['AES']
    mode: Literal['CBC', 'GCM']

    def __init__(
        self,
        name: str,
        bits: int,
        cipher: Literal['AES'],
        mode: Literal['CBC', 'GCM']
    ):
        self.bits = bits
        self.cipher = cipher
        self.name = name
        self.mode = mode