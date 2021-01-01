from snek.constants import HttpStatusCode
from snek.models import VaultResponse


class TestVaultResponse:
    def test__init__(self):
        vr = VaultResponse({}, 200)
        assert vr.status_code == HttpStatusCode.SUCCESS_DATA
        vr = VaultResponse({}, HttpStatusCode(403))
        vr.response == {}
        vr.errors is None
        assert vr.status_code == HttpStatusCode.FORBIDDEN

    def test_ok(self):
        vr = VaultResponse({}, status_code=200)
        assert vr.ok
        vr.status_code = HttpStatusCode(500)
        assert not vr.ok
