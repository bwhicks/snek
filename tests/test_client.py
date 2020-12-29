import pytest
from requests.cookies import morsel_to_cookie
from snek.client import VaultClient
from snek.constants import HttpMethod, HttpStatusCode
from snek.errors import VaultClientException


@pytest.fixture
def mock_http_call(mocker):
    return mocker.patch("snek.client.requests.Session.request")


@pytest.fixture
def mock_client(mock_request):
    return VaultClient("http://localhost:8200/", "abc123")


@pytest.fixture
def mock_request(mocker):
    return mocker.patch("snek.client.VaultClient.make_request")


@pytest.mark.vault
def test_make_request(test_client):
    res = test_client.make_request(
        "GET",
        f"{test_client.vault_addr}v1/sys/init",
        params={"X-Vault-Token": None},
    )
    assert res.status_code == HttpStatusCode.SUCCESS_DATA
    assert res.response["initialized"] is True


def test_make_request_error(mock_http_call):
    mock_http_call.side_effect = IOError("Connection failure")
    client = VaultClient("http://localhost:8200/", "abc123")
    with pytest.raises(VaultClientException, match="Connection failure"):
        client.make_request(
            HttpMethod.GET.value,
            "http://localhost:8200/v1/sys/init",
            params={"X-Vault-Token": None},
        )


def test_make_request_bad_code(mocker, mock_http_call):
    mock_http_call.return_value = mocker.Mock()
    mock_http_call.return_value.status_code = HttpStatusCode.FORBIDDEN.value
    mock_http_call.return_value.json.return_value = {"foo": "bar"}
    client = VaultClient("http://localhost:8200/", "abc123")
    with pytest.raises(VaultClientException, match='{"foo": "bar"}'):
        client.make_request(
            HttpMethod.GET.value,
            "http://localhost:8200/v1/sys/init",
            params={"X-Vault-Token": None},
        )


def test_get(mock_client):
    res = mock_client.get("/v1/sys/madeup", params={"foo": "bar"})
    assert res is mock_client.make_request.return_value
    mock_client.make_request.assert_called_with(
        HttpMethod.GET.value,
        "http://localhost:8200/v1/sys/madeup",
        params={"foo": "bar"},
    )


def test_put(mock_client):
    res = mock_client.put("/v1/sys/madeup", data={"foo": "bar"})
    assert res is mock_client.make_request.return_value
    mock_client.make_request.assert_called_with(
        HttpMethod.PUT.value, "http://localhost:8200/v1/sys/madeup", json={"foo": "bar"}
    )


def test_post(mock_client):
    res = mock_client.post("/v1/sys/madeup", data={"foo": "bar"})
    assert res is mock_client.make_request.return_value
    mock_client.make_request.assert_called_with(
        HttpMethod.POST.value,
        "http://localhost:8200/v1/sys/madeup",
        json={"foo": "bar"},
    )


def test_list(mock_client):
    res = mock_client.list("/v1/sys/madeup", params={"foo": "bar"})
    assert res is mock_client.make_request.return_value
    mock_client.make_request.assert_called_with(
        HttpMethod.LIST.value,
        "http://localhost:8200/v1/sys/madeup",
        params={"foo": "bar"},
    )
