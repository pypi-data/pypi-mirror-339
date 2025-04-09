import functools
from typing import Any

import pydantic
from libcanonical.types import Base64
from libcanonical.utils.encoding import b64encode

from canonical.ext.jose.types import JSONWebAlgorithm
from ._jsonwebkey import JSONWebKey
from ._jwsheader import JWSHeader


class Signature(pydantic.BaseModel):
    protected: Base64 | None = None
    header: dict[str, Any] = {}
    signature: Base64

    @property
    def alg(self):
        # The alg parameter is mandatory.
        return JSONWebAlgorithm.validate(self.claims['alg'])

    @functools.cached_property
    def claims(self):
        return {
            **self.header,
            **self._header.model_dump(exclude_defaults=True, exclude_none=True)
        }

    @functools.cached_property
    def _header(self):
        assert self.protected
        return JWSHeader.model_validate_json(self.protected)

    @classmethod
    async def create(
        cls,
        signer: JSONWebKey,
        alg: JSONWebAlgorithm,
        payload: bytes,
        typ: str | None = None,
        kid: str | None = None
    ):
        protected = JWSHeader(alg=alg, typ=typ, kid=kid)
        return cls.model_validate({
            'protected': bytes(protected),
            'signature': await protected.sign(signer, payload=payload)
        })

    def is_valid(self):
        """Return a boolean indicating if the JWS conforms to the
        specification.
        """
        return all([
            bool(self.claims.get('alg'))
        ])

    async def verify(self, verifier: JSONWebKey, payload: bytes):
        assert self.protected is not None
        message = bytes.join(b'.', [b64encode(self.protected), payload])
        return await verifier.verify(self.signature, message, self.alg)