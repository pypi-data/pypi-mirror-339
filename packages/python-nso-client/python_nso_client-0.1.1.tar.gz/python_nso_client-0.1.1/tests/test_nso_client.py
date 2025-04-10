import httpx
import pytest
from pytest_httpx import HTTPXMock

from fixtures import (
    MOCK_BB,
    MOCK_RESP_400_INVALID_PARAM,
    MOCK_RESP_400_MISSING_MODULE,
    MOCK_RESP_401_ACCESS_DENIED,
    MOCK_RESP_404_KEYPATH,
    MOCK_RESP_404_NOT_FOUND,
    MOCK_RESP_CHECK_SYNC,
    MOCK_RESP_DRY_RUN,
)
from nso_client import (
    AccessDeniedError,
    BadRequestError,
    DryRunResult,
    NotFoundError,
    NSOClient,
)


def test_get_200(httpx_mock: HTTPXMock):
    """Test a normal GET request"""
    # Setup mock
    httpx_mock.add_response(
        url=httpx.URL(
            "https://localhost/restconf/data/tailf-ncs:services/bb:backbone=my-bb-1",
            params={"content": "config"},
        ),
        json={"bb:backbone": [MOCK_BB]},
    )

    # Execute
    n = NSOClient("https://localhost")
    resp = n.get("/tailf-ncs:services/bb:backbone={}", "my-bb-1", content="config")

    # Check
    assert len(resp["bb:backbone"]) == 1
    assert resp["bb:backbone"][0]["name"] == "my-bb-1"
    assert resp["bb:backbone"][0]["admin-state"] == "in-service"
    assert len(httpx_mock.get_requests()) == 1


def test_get_400_missing_module(httpx_mock: HTTPXMock):
    """A path that's invalid because there's no YANG module loaded for it"""
    # Setup
    httpx_mock.add_response(
        url="https://localhost/restconf/data/foo/bar",
        status_code=400,
        json=MOCK_RESP_400_MISSING_MODULE,
    )

    # Execute
    nso = NSOClient("https://localhost")
    with pytest.raises(BadRequestError):
        nso.get("/foo/bar")

    # Check
    assert len(httpx_mock.get_requests()) == 1


def test_get_400_invalid_query_params(httpx_mock: HTTPXMock):
    """Passing a query parameter that's not valid"""
    # Setup
    httpx_mock.add_response(
        url="https://localhost/restconf/data/tailf-ncs:services/bb:backbone=my-bb-1?foo=bar",
        status_code=400,
        json=MOCK_RESP_400_INVALID_PARAM,
    )

    # Execute
    nso = NSOClient("https://localhost")
    with pytest.raises(BadRequestError):
        nso.get("/tailf-ncs:services/bb:backbone={}", "my-bb-1", foo="bar")

    # Check
    assert len(httpx_mock.get_requests()) == 1
    print(httpx_mock.get_requests())


def test_get_401_access_denied(httpx_mock: HTTPXMock):
    """Get a path we don't have access to"""
    # Setup
    httpx_mock.add_response(
        url="https://localhost/restconf/data/tailf-ncs:services/bb:backbone=my-bb-1",
        status_code=401,
        json=MOCK_RESP_401_ACCESS_DENIED,
    )

    # Execute
    nso = NSOClient("https://localhost")
    with pytest.raises(AccessDeniedError):
        nso.get("/tailf-ncs:services/bb:backbone={}", "my-bb-1")

    # Check
    assert len(httpx_mock.get_requests()) == 1


def test_get_404_not_found(httpx_mock: HTTPXMock):
    """Path is syntactically valid, there's just no object there"""
    # Setup
    httpx_mock.add_response(
        url="https://localhost/restconf/data/tailf-ncs:services/bb:backbone=my-bb-1",
        status_code=404,
        json=MOCK_RESP_404_NOT_FOUND,
    )

    # Execute
    n = NSOClient("https://localhost")
    resp = n.get("/tailf-ncs:services/bb:backbone={}", "my-bb-1")

    # Check
    assert len(httpx_mock.get_requests()) == 1
    assert resp is None


def test_put_200(httpx_mock: HTTPXMock):
    """Normal create"""
    # Setup Mock
    httpx_mock.add_response(
        method="PUT",
        url=httpx.URL(
            "https://localhost/restconf/data/tailf-ncs:services/bb:backbone=my-bb-1",
        ),
        status_code=204,
        content="",
    )

    # Execute
    n = NSOClient("https://localhost")
    resp = n.put(
        "/tailf-ncs:services/bb:backbone={}",
        "my-bb-1",
        payload={"bb:backbone": [MOCK_BB]},
    )

    # Check
    assert resp is None
    assert len(httpx_mock.get_requests()) == 1


# PUT will have response content (dry-run)
def test_put_200_dry_run(httpx_mock: HTTPXMock):
    """dry-run create with CLI output"""
    # Setup
    httpx_mock.add_response(
        method="PUT",
        url=httpx.URL(
            "https://localhost/restconf/data/tailf-ncs:services/bb:backbone=my-bb-1",
            params={"dry-run": "cli"},
        ),
        match_json={"bb:backbone": [MOCK_BB]},
        json=MOCK_RESP_DRY_RUN,
    )

    # Execute
    n = NSOClient("https://localhost")
    resp = n.put(
        "/tailf-ncs:services/bb:backbone={}",
        MOCK_BB["name"],
        payload={"bb:backbone": [MOCK_BB]},
        dry_run="cli",
    )

    # Check
    assert isinstance(resp, DryRunResult)
    assert resp.dry_run is DryRunResult.DryRunType.CLI
    assert resp.changes["local-node"]
    assert len(httpx_mock.get_requests()) == 1


# Delete an object
def test_delete_200(httpx_mock: HTTPXMock):
    # Setup mock
    httpx_mock.add_response(
        method="DELETE",
        url=httpx.URL(
            "https://localhost/restconf/data/tailf-ncs:services/bb:backbone=my-bb-1",
        ),
    )

    # Execute
    nso = NSOClient("https://localhost")
    resp = nso.delete("/tailf-ncs:services/bb:backbone={}", "my-bb-1")

    # Check
    assert len(httpx_mock.get_requests()) == 1
    assert resp is None


def test_delete_404_path(httpx_mock: HTTPXMock):
    """Delete an object that has already been deleted"""
    # Setup
    httpx_mock.add_response(
        url="https://localhost/restconf/data/tailf-ncs:services/bb:backbone=does-not-exist",
        status_code=404,
        method="DELETE",
        json=MOCK_RESP_404_KEYPATH,
    )

    # Execute
    nso = NSOClient("https://localhost")
    with pytest.raises(NotFoundError):
        nso.delete("/tailf-ncs:services/bb:backbone=does-not-exist")

    # Check
    assert len(httpx_mock.get_requests()) == 1


# Check a successful action
def test_post_200_check_sync(httpx_mock: HTTPXMock):
    # Setup Mocks
    httpx_mock.add_response(
        method="POST",
        url=httpx.URL(
            "https://localhost/restconf/data/tailf-ncs:devices/check-sync",
        ),
        status_code=204,
        match_json={},
        json=MOCK_RESP_CHECK_SYNC,
    )

    # Execute
    n = NSOClient("https://localhost")
    resp = n.post("/tailf-ncs:devices/check-sync", payload={})

    # Check
    assert len(httpx_mock.get_requests()) == 1
    assert "tailf-ncs:output" in resp
    assert "sync-result" in resp["tailf-ncs:output"]
    assert resp["tailf-ncs:output"]["sync-result"] == [
        {
            "device": "mock-dev1",
            "result": "in-sync",
        }
    ]
