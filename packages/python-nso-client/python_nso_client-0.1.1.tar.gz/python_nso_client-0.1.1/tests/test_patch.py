import pytest
from pytest_httpx import HTTPXMock

from fixtures import (
    HEADER_YANG_PATCH,
    MOCK_BB,
    MOCK_RESP_PATCH_ALREADY_EXISTS,
    MOCK_RESP_PATCH_DRY_RUN,
    MOCK_RESP_PATCH_OUT_OF_SYNC,
    MOCK_RESP_PATCH_SUCCESS,
)
from nso_client import DryRunResult, NSOClient
from nso_client.exceptions import PatchError, YangPatchError
from nso_client.types import InsertWhere


def test_patch_merge_200(httpx_mock: HTTPXMock):
    """
    Single yang patch merge that succeeds
    """
    # Setup
    httpx_mock.add_response(
        url="https://localhost/restconf/data/tailf-ncs:services",
        method="PATCH",
        match_headers=HEADER_YANG_PATCH,
        match_json={
            "ietf-yang-patch:yang-patch": {
                "patch-id": "/tailf-ncs:services",
                "edit": [
                    {
                        "edit-id": "/bb:backbone=my-bb-1",
                        "operation": "merge",
                        "target": "/bb:backbone=my-bb-1",
                        "value": MOCK_BB,
                    }
                ],
            }
        },
        json=MOCK_RESP_PATCH_SUCCESS,
    )

    # Execute
    nso = NSOClient("https://localhost")
    p = nso.yang_patch("/tailf-ncs:services")
    p.merge("/bb:backbone={}", "my-bb-1", value=MOCK_BB)
    p.commit()

    # Check
    assert len(httpx_mock.get_requests()) == 1


def test_patch_create_200(httpx_mock: HTTPXMock):
    """Test create instead of merge"""

    # Setup
    httpx_mock.add_response(
        url="https://localhost/restconf/data/tailf-ncs:services",
        method="PATCH",
        status_code=200,
        match_headers=HEADER_YANG_PATCH,
        match_json={
            "ietf-yang-patch:yang-patch": {
                "patch-id": "/tailf-ncs:services",
                "edit": [
                    {
                        "edit-id": "/bb:backbone=my-bb-1",
                        "operation": "create",
                        "target": "/bb:backbone=my-bb-1",
                        "value": MOCK_BB,
                    }
                ],
            }
        },
        json=MOCK_RESP_PATCH_SUCCESS,
    )

    # Execute
    nso = NSOClient("https://localhost")
    p = nso.yang_patch("/tailf-ncs:services")
    p.create("/bb:backbone={}", "my-bb-1", value=MOCK_BB)
    p.commit()

    # Check
    assert len(httpx_mock.get_requests()) == 1


def test_patch_create_409_already_exists(httpx_mock: HTTPXMock):
    """Path is valid, but there's an error with the object"""

    # Setup
    httpx_mock.add_response(
        method="PATCH",
        url="https://localhost/restconf/data/tailf-ncs:services",
        status_code=409,
        match_headers=HEADER_YANG_PATCH,
        match_json={
            "ietf-yang-patch:yang-patch": {
                "patch-id": "/tailf-ncs:services",
                "edit": [
                    {
                        "edit-id": "/bb:backbone=my-bb-1",
                        "operation": "create",
                        "target": "/bb:backbone=my-bb-1",
                        "value": MOCK_BB,
                    }
                ],
            }
        },
        json=MOCK_RESP_PATCH_ALREADY_EXISTS,
    )

    # Execute
    nso = NSOClient("https://localhost")
    p = nso.yang_patch("/tailf-ncs:services")
    p.create("/bb:backbone={}", "my-bb-1", value=MOCK_BB)
    result = p.commit()

    # Check
    assert len(httpx_mock.get_requests()) == 1
    with pytest.raises(PatchError):
        result.raise_if_error()


def test_patch_create_dry_run_200(httpx_mock: HTTPXMock):
    """Check that the output of a dry-run is valid"""
    # Setup

    httpx_mock.add_response(
        method="PATCH",
        url="https://localhost/restconf/data/tailf-ncs:services?dry-run=cli",
        match_headers=HEADER_YANG_PATCH,
        match_json={
            "ietf-yang-patch:yang-patch": {
                "patch-id": "/tailf-ncs:services",
                "edit": [
                    {
                        "edit-id": "/bb:backbone=my-bb-1",
                        "operation": "create",
                        "target": "/bb:backbone=my-bb-1",
                        "value": MOCK_BB,
                    }
                ],
            }
        },
        json=MOCK_RESP_PATCH_DRY_RUN,
    )

    # Execute
    nso = NSOClient("https://localhost")
    p = nso.yang_patch("/tailf-ncs:services")
    p.create("/bb:backbone={}", "my-bb-1", value=MOCK_BB)
    resp = p.commit(dry_run="cli")

    # Check that the response read correctly
    assert type(resp) is DryRunResult
    assert resp.dry_run == DryRunResult.DryRunType.CLI
    assert resp.changes["local-node"] == "Some changes"

    # Check that the call was made correctly
    assert len(httpx_mock.get_requests()) == 1


def test_patch_replace_200(httpx_mock: HTTPXMock):
    """Test replace"""

    # Setup
    httpx_mock.add_response(
        url="https://localhost/restconf/data/tailf-ncs:services",
        method="PATCH",
        match_headers=HEADER_YANG_PATCH,
        match_json={
            "ietf-yang-patch:yang-patch": {
                "patch-id": "/tailf-ncs:services",
                "edit": [
                    {
                        "edit-id": "/bb:backbone=my-bb-1",
                        "operation": "replace",
                        "target": "/bb:backbone=my-bb-1",
                        "value": MOCK_BB,
                    }
                ],
            }
        },
        json=MOCK_RESP_PATCH_SUCCESS,
    )

    # Execute
    nso = NSOClient("https://localhost")
    p = nso.yang_patch("/tailf-ncs:services")
    p.replace("/bb:backbone={}", "my-bb-1", value=MOCK_BB)
    p.commit()

    # Check
    assert len(httpx_mock.get_requests()) == 1


def test_patch_delete_200(httpx_mock: HTTPXMock):
    """Test delete"""
    # Setup
    httpx_mock.add_response(
        url="https://localhost/restconf/data/tailf-ncs:services",
        method="PATCH",
        match_headers=HEADER_YANG_PATCH,
        match_json={
            "ietf-yang-patch:yang-patch": {
                "patch-id": "/tailf-ncs:services",
                "edit": [
                    {
                        "edit-id": "/bb:backbone=my-bb-1",
                        "operation": "delete",
                        "target": "/bb:backbone=my-bb-1",
                    }
                ],
            }
        },
        json=MOCK_RESP_PATCH_SUCCESS,
    )

    # Execute
    nso = NSOClient("https://localhost")
    p = nso.yang_patch("/tailf-ncs:services")
    p.delete("/bb:backbone={}", "my-bb-1")
    p.commit()

    # Check
    assert len(httpx_mock.get_requests()) == 1


def test_patch_insert_200(httpx_mock: HTTPXMock):
    """Test one of each and every options"""
    # Setup
    httpx_mock.add_response(
        url="https://localhost/restconf/data/tailf-ncs:services",
        method="PATCH",
        match_headers=HEADER_YANG_PATCH,
        match_json={
            "ietf-yang-patch:yang-patch": {
                "patch-id": "/tailf-ncs:services",
                "edit": [
                    {
                        "edit-id": "/bb:backbone=my-bb-1",
                        "operation": "insert",
                        "where": "after",
                        "point": "/bb:backbone=my-bb-0",
                        "target": "/bb:backbone=my-bb-1",
                        "value": MOCK_BB,
                    }
                ],
            }
        },
        json=MOCK_RESP_PATCH_SUCCESS,
    )

    # Execute
    nso = NSOClient("https://localhost")
    p = nso.yang_patch("/tailf-ncs:services")
    p.insert(
        "/bb:backbone={}",
        "my-bb-1",
        where=InsertWhere.AFTER,
        point="/bb:backbone=my-bb-0",
        value=MOCK_BB,
    )
    p.commit()

    # Check
    assert len(httpx_mock.get_requests()) == 1


def test_patch_move_200(httpx_mock: HTTPXMock):
    """Test one of each and every options"""
    # Setup
    httpx_mock.add_response(
        url="https://localhost/restconf/data/tailf-ncs:services",
        method="PATCH",
        match_headers=HEADER_YANG_PATCH,
        match_json={
            "ietf-yang-patch:yang-patch": {
                "patch-id": "/tailf-ncs:services",
                "edit": [
                    {
                        "edit-id": "/bb:backbone=my-bb-1",
                        "operation": "move",
                        "where": "after",
                        "point": "/bb:backbone=my-bb-0",
                        "target": "/bb:backbone=my-bb-1",
                    }
                ],
            }
        },
        json=MOCK_RESP_PATCH_SUCCESS,
    )

    # Execute
    nso = NSOClient("https://localhost")
    p = nso.yang_patch("/tailf-ncs:services")
    p.move(
        "/bb:backbone={}",
        "my-bb-1",
        where=InsertWhere.AFTER,
        point="/bb:backbone=my-bb-0",
    )
    p.commit()

    # Check
    assert len(httpx_mock.get_requests()) == 1


def test_patch_replace_400_out_of_sync(httpx_mock: HTTPXMock):
    """Check that "out-of-sync" errors are returned"""
    # Setup
    httpx_mock.add_response(
        url="https://localhost/restconf/data/tailf-ncs:services",
        method="PATCH",
        status_code=400,
        match_headers=HEADER_YANG_PATCH,
        match_json={
            "ietf-yang-patch:yang-patch": {
                "patch-id": "/tailf-ncs:services",
                "edit": [
                    {
                        "edit-id": "/bb:backbone=my-bb-1",
                        "operation": "replace",
                        "target": "/bb:backbone=my-bb-1",
                        "value": MOCK_BB,
                    }
                ],
            }
        },
        json=MOCK_RESP_PATCH_OUT_OF_SYNC,
    )

    # Execute
    nso = NSOClient("https://localhost")
    p = nso.yang_patch("/tailf-ncs:services")
    p.replace("/bb:backbone={}", "my-bb-1", value=MOCK_BB)

    # Check
    with pytest.raises(YangPatchError, match=r"out of sync"):
        p.commit()
    assert len(httpx_mock.get_requests()) == 1
