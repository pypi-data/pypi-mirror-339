"""Mock fixture data"""

HEADER_YANG_PATCH = {"Content-Type": "application/yang-patch+json"}

# Example backbone service
MOCK_BB = {
    "name": "my-bb-1",
    "links": [
        {"device": "xr0", "interface": "TenGigE0/0/0"},
        {"device": "xr1", "interface": "TenGigE0/0/1"},
    ],
    "metric": 500,
    "admin-state": "in-service",
}

# Various responses
MOCK_RESP_DRY_RUN = {
    "dry-run-result": {
        "cli": {
            "local-node": {"data": "Mock dry-run data"},
        }
    }
}
MOCK_RESP_CHECK_SYNC = {
    "tailf-ncs:output": {
        "sync-result": [
            {"device": "mock-dev1", "result": "in-sync"},
        ]
    }
}
MOCK_RESP_404_NOT_FOUND = {
    "ietf-restconf:errors": {
        "error": [
            {
                "error-type": "application",
                "error-tag": "invalid-value",
                "error-message": "uri keypath not found",
            }
        ]
    }
}
MOCK_RESP_404_KEYPATH = {
    "ietf-restconf:errors": {
        "error": [
            {
                "error-type": "application",
                "error-tag": "invalid-value",
                "error-message": "uri keypath not found",
            }
        ]
    }
}
MOCK_RESP_400_MISSING_MODULE = {
    "ietf-restconf:errors": {
        "error": [
            {
                "error-type": "application",
                "error-tag": "missing-attribute",
                "error-message": "missing module name for 'foo'",
            }
        ]
    }
}
MOCK_RESP_400_INVALID_PARAM = {
    "ietf-restconf:errors": {
        "error": [
            {
                "error-type": "application",
                "error-tag": "invalid-value",
                "error-message": "invalid query parameter: foo",
            }
        ]
    }
}
MOCK_RESP_401_ACCESS_DENIED = {
    "ietf-restconf:errors": {
        "error": [{"error-type": "protocol", "error-tag": "access-denied"}]
    }
}
MOCK_RESP_PATCH_SUCCESS = {
    "ietf-yang-patch:yang-patch-status": {
        "patch-id": "mock-patch-id",
        "ok": [None],
    }
}
MOCK_RESP_PATCH_DRY_RUN = {
    "dry-run-result": {"cli": {"local-node": {"data": "Some changes"}}}
}

# YANG-Patch responses
MOCK_RESP_PATCH_ALREADY_EXISTS = {
    "ietf-yang-patch:yang-patch-status": {
        "patch-id": "setup-services",
        "edit-status": {
            "edit": [
                {
                    "edit-id": "/bb:backbone=my-bb-1",
                    "errors": {
                        "error": [
                            {
                                "error-type": "application",
                                "error-tag": "data-exists",
                                "error-path": "/tailf-ncs:services/bb:backbone[name='my-bb-1']",
                                "error-message": "object already exists: /tailf-ncs:services/bb:backbone[name='my-bb-1']",
                            }
                        ]
                    },
                }
            ]
        },
    }
}
MOCK_RESP_PATCH_OUT_OF_SYNC = {
    "ietf-yang-patch:yang-patch-status": {
        "patch-id": "/",
        "edit-status": {
            "edit": [
                {
                    "edit-id": "/bb:backbone=my-bb-1",
                    "errors": {
                        "error": [
                            {
                                "error-tag": "malformed-message",
                                "error-message": "Network Element Driver: device core1.mock: out of sync",
                            }
                        ]
                    },
                }
            ]
        },
    }
}
