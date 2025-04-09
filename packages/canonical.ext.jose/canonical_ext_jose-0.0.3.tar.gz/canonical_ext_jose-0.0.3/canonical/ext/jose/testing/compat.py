from typing import Any
from typing import Awaitable
from typing import Callable

import pytest

from canonical.ext.jose.models import JSONWebEncryption
from canonical.ext.jose.models import JSONWebKeySet
from canonical.ext.jose.models import JSONWebKey
from canonical.ext.jose.types import ContentEncryptionAlgorithm
from canonical.ext.jose.types import JSONWebAlgorithm


__all__: list[str] = [
    'test_compat_jwt_jwe_their_encryption_our_decryption'
]


JWE_ALGORITHMS = [
    JSONWebAlgorithm.validate('RSA-OAEP-256'),
    JSONWebAlgorithm.validate('RSA-OAEP-384'),
    JSONWebAlgorithm.validate('RSA-OAEP-512'),
    JSONWebAlgorithm.validate('A128KW'),
    JSONWebAlgorithm.validate('A192KW'),
    JSONWebAlgorithm.validate('A256KW'),
    JSONWebAlgorithm.validate('ECDH-ES+A128KW'),
    JSONWebAlgorithm.validate('ECDH-ES+A192KW'),
    JSONWebAlgorithm.validate('ECDH-ES+A256KW'),
    JSONWebAlgorithm.validate('A128GCMKW'),
    JSONWebAlgorithm.validate('A192GCMKW'),
    JSONWebAlgorithm.validate('A256GCMKW'),
]

JWE_DIRECT_ALGORITHMS = [
    JSONWebAlgorithm.validate('ECDH-ES'),
    JSONWebAlgorithm.validate('dir'),
]

JWE_CEK_ALGORITHMS = [
    ContentEncryptionAlgorithm('A128GCM'),
    ContentEncryptionAlgorithm('A192GCM'),
    ContentEncryptionAlgorithm('A256GCM'),
]


@pytest.mark.parametrize("alg", JWE_ALGORITHMS)
@pytest.mark.parametrize("enc", JWE_CEK_ALGORITHMS)
@pytest.mark.asyncio
async def test_compat_jwt_jwe_their_encryption_our_decryption(
    jwe_factory: Callable[
        [
            JSONWebAlgorithm,
            ContentEncryptionAlgorithm,
            list[JSONWebKey],
            dict[str, Any] | bytes
        ],
        Awaitable[str]
    ],
    alg: JSONWebAlgorithm,
    enc: ContentEncryptionAlgorithm,
    jwks: JSONWebKeySet
):
    key = jwks.get(alg)
    if key is None:
        pytest.skip(
            f"No test key specified for {alg}. Available keys "
            f"are: {str.join(',', [str(x.kid) for x in jwks.keys])}"
        )
    serialized, ipt = await jwe_factory(alg, enc, [key], {'iss': 'https://jose.example'})
    jwe = JSONWebEncryption.model_validate(serialized)
    opt = await jwe.decrypt(key)
    assert opt == ipt