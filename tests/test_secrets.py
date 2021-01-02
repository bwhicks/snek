import pytest
from snek.constants import HttpStatusCode
from snek.exceptions import SecretCreateUpdateException, SecretReadException
from snek.secrets import KVSecretV2, KVSecretV2API


@pytest.fixture
def test_kv2(test_client):
    return KVSecretV2API(test_client)


class TestKVSecretV2:
    def test__str__(self):
        secret = KVSecretV2("/foo/bar")
        assert str(secret) == "/foo/bar: null"

    def test_create_or_update(self, test_kv2):
        assert test_kv2.create_or_update("foo/bar", {"foo": "bar"})

    def test_create_or_update_cas_works(self, test_kv2):
        test_kv2.create_or_update("foo/bar", {"foo": "bar"})
        with pytest.raises(SecretCreateUpdateException):
            assert test_kv2.create_or_update("foo/bar", {"foo": "bar"}, 0)

    def test_read(self, test_kv2):
        secret = test_kv2.create_or_update("foo/bar", {"foo": "bar", "baz": "bam"})
        read_secret = test_kv2.read(secret.path)
        assert read_secret.value == {"foo": "bar", "baz": "bam"}

    def test_read_raises_error(self, test_kv2):
        with pytest.raises(SecretReadException):
            test_kv2.read("foo/bar")

    def test_configure_secret_engine(self, test_kv2):
        test_kv2.configure()
        res = test_kv2.configure(max_versions=3)
        assert res.status_code == HttpStatusCode.SUCCESS_NO_DATA

    def test_empty_secret(self):
        kv2 = KVSecretV2("foo/bar")
        assert kv2.data is None
