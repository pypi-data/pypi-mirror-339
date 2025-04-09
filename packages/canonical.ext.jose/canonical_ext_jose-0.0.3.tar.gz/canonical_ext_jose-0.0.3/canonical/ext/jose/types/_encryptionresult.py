from typing import TYPE_CHECKING

import pydantic

if TYPE_CHECKING:
    from canonical.ext.jose.models import JWEHeader


class EncryptionResult(pydantic.BaseModel):
    ct: bytes = pydantic.Field(
        default=...
    )

    iv: bytes = pydantic.Field(
        default_factory=bytes
    )

    tag: bytes = pydantic.Field(
        default_factory=bytes
    )

    aad: bytes = pydantic.Field(
        default_factory=bytes
    )

    def add_to_header(self, header: 'JWEHeader') -> None:
        pass

    async def _await(self):
        return self

    def __await__(self):
        return self._await().__await__()

    def __bytes__(self):
        return self.ct