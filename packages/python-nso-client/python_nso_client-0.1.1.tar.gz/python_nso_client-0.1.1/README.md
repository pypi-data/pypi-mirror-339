# Python NSO Library

Thin wrapper around RestConf designed to interact with NSO.

**Key Features:**

- Detect errors raising meaningful exceptions
- Parameter support in URL to avoid URL Encoding mistakes
- Support for generating and executing YANG Patches
- Handling of dry-run responses

## Usage

Installing

```sh
uv add python-nso-client
```

Writing code with nso_client

```py
from nso_client import NSOClient
from httpx import BasicAuth

nso = NSOClient(
    "https://localhost",
    auth=BasicAuth("acct", "secret")
)

# Fetching data
resp = nso.get("/tailf-ncs:services/bb:backbone", content="config")
for bb in resp["bb:backbone"]:
    print(bb)


# Create objects
resp = nso.put(
    "/tailf-ncs:services/bb:backbone={}",
    "my-bb-1",
    payload={
        "bb:backbone": [
            {
                "name": "my-bb-1",
                "links": [
                    {"device": "xr0", "interface": "TenGigE0/0/0"},
                    {"device": "xr1", "interface": "TenGigE0/0/1"},
                ],
                "metric": 500,
                "admin-state": "in-service",
            }
        ]
    },
)

# Using yang-patch to modify multiple areas in the same transaction
patch = nso.yang_patch("/tailf-ncs:services")
patch.merge("/bb:backbone={}", "my-bb-1", value=...)
patch.merge("/bb:backbone={}", "my-bb-2", value=...)
patch.delete("/bb:backbone={}", "my-bb-3")
resp = patch.commit(dry_run="cli")
print(resp.changes)
patch.commit()

# Error handling
try:
    nso.delete("/tailf-ncs:services/bb:backbone={}", "does-not-exist")
except NotFoundError as exc:
    print("Backbone already deleted", exc)

# Fetching results in a None, not an exception
resp = nso.get("/tailf-ncs:services/bb:backbone={}", "does-not-exist")
assert resp is None
```

## Developing

```sh
# Build
uv build
```
