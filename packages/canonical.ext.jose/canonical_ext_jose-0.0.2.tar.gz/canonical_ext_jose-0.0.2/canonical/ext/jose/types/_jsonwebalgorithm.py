from libcanonical.types import StringType

from ._jsonwebalgorithmconfig import JSONWebAlgorithmConfig


class JSONWebAlgorithm(StringType):
    config: JSONWebAlgorithmConfig

    @classmethod
    def validate(cls, v: str):
        self = cls(v)
        self.config = JSONWebAlgorithmConfig.get(self)
        return self

    def wraps(self):
        return self.config.mode not in {
            'DIRECT_ENCRYPTION',
            'DIRECT_KEY_AGREEMENT'
        }