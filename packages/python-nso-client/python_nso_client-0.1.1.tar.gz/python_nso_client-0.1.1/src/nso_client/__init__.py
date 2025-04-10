"""
Utility library to make talking with NSO slightly simpler

It's a thin wrapper around `requests` that handles some common parameters
a user would want to pass and encodes correctly.
"""

from __future__ import annotations

import ssl
import urllib.parse
from dataclasses import dataclass
from enum import Enum

import httpx
import structlog
from httpx import BasicAuth
from structlog.stdlib import BoundLogger

from nso_client.exceptions import (
    AccessDeniedError,
    BadRequestError,
    NotFoundError,
    PatchError,
    RestConfError,
    YangPatchError,
)
from nso_client.types import ContentType, InsertWhere, PatchType

__all__ = [
    "NSOClient",
    "Patch",
    "PatchResult",
    "RestConfError",
    "NotFoundError",
    "AccessDeniedError",
    "BadRequestError",
]


class NSOCommitMode(Enum):
    NORMAL = "normal"
    DRY_RUN = "dry-run"
    NO_DEPLOY = "no-deploy"

    @classmethod
    def _missing_(cls, value: str):
        raise Exception(
            f"{value} is not a valid {cls.__name__}"
            f"valid options are {cls._member_names_}"
        )


class NSOClient:
    """
    Lite wrapper that instantiates an NSO connector object
    with secrets from environment variables.
    """

    session: httpx.Client
    nso_url: str
    log: BoundLogger
    commit_kwargs: dict[str, str]

    def __init__(
        self,
        nso_url: str,
        auth: BasicAuth | None = None,
        verify: bool | ssl.SSLContext = True,
        restconf_path: str = "/restconf/data",
        logger: BoundLogger = None,
        **commit_kwargs,
    ):
        """
        Create a light weight NSO Client

        base_url:       NSO server, IE: https://nso.internal
        auth:           Authentication object to pass to httpx.Client
        verify_ssl:     Verify SSL or not
        restconf_path:  Restconf base path, this is almost always /restconf/data
        logger:         Logger to use for queries
        commit_kwargs:  Additional parameters to pass to any given commit
        """
        self.session = httpx.Client(
            verify=verify,
            auth=auth,
            headers={
                "Accept": ContentType.YANG_DATA,
                "Content-Type": ContentType.YANG_DATA,
            },
        )
        self.nso_url = nso_url + restconf_path
        if not logger:
            logger = structlog.get_logger()
        self.log = logger.bind(lib="NSOClient")
        self.commit_kwargs = commit_kwargs

    def get(
        self,
        path: str,
        *path_params: list[str],
        **kwargs,
    ) -> list | dict:
        """
        Retrieve RestConf data at path.

        path:           A restconf path. Example: /common:infrastructure/prefix-set:prefix-set={}
        path_params:    Values to insert into `{}` in the URL. Values will be appropriately
                        URL encoded, so "Foo/Bar" will be encoded to "Foo%2FBar"
        kwargs:         Query keyword arguments, see query_params()

        Returns:        JSON Payload, or raises an exception if an error occurred
        Raises:         RestConfError or a sub-class
        """
        url = self._make_url(path, path_params)
        query_params = self.query_params(**kwargs)
        response = self.session.get(url, params=query_params)
        self.log.debug(
            "NSO Query",
            method="GET",
            url=url,
            params=query_params,
            status_code=response.status_code,
            ok=response.is_success,
            error_text=None if response.is_success else response.text,
            response_len=len(response.content),
            elapsed_time=response.elapsed.total_seconds(),
        )
        # Special case for .get() - if we get a 404, just return None instead
        # of raising a NotFound exception
        if response.status_code == 404:
            return None
        return self._parse_response(response)

    def put(
        self,
        path: str,
        *path_params: list[str],
        payload: dict[str, str],
        **kwargs,
    ) -> None | DryRunResult:
        """
        PUT data at a given path

        path:           A restconf path. Example: /common:infrastructure/prefix-set:prefix-set={}
        path_params:    Values to insert into `{}` in the URL. Values will be appropriately
                        URL encoded, so "Foo/Bar" will be encoded to "Foo%2FBar"
        kwargs:         Query keyword arguments, see query_params()


        Returns:        JSON Payload, or raises an exception if an error occurred
        Raises:         RestConfError or a sub-class
        """
        url = self._make_url(path, path_params)
        query_params = self.query_params(**kwargs)
        response = self.session.put(url, params=query_params, json=payload)
        self.log.info(
            "NSO Commit",
            method="PUT",
            url=url,
            params=query_params,
            payload=payload,
            status_code=response.status_code,
            ok=response.is_success,
            error_text=None if response.is_success else response.text,
            response_len=len(response.content),
            elapsed_time=response.elapsed.total_seconds(),
        )
        return self._parse_response(response)

    def delete(
        self,
        path: str,
        *path_params: list[str],
        **kwargs,
    ) -> None | DryRunResult:
        """
        DELETE data to a given path

        path:           A restconf path. Example: /ncs:devices/device/check-sync
        path_params:    Values to insert into `{}` in the URL. Values will be appropriately
                        URL encoded, so "Foo/Bar" will be encoded to "Foo%2FBar"
        kwargs:         Query keyword arguments, see query_params()

        Returns:        None, dict if dry_run is used
        Raises:         RestConfError or a sub-class
        """
        url = self._make_url(path, path_params)
        query_params = self.query_params(**kwargs)
        response = self.session.delete(url, params=query_params)
        self.log.info(
            "NSO Commit",
            method="DELETE",
            url=url,
            params=query_params,
            status_code=response.status_code,
            ok=response.is_success,
            error_text=None if response.is_success else response.text,
            response_len=len(response.content),
            elapsed_time=response.elapsed.total_seconds(),
        )
        return self._parse_response(response)

    def post(
        self,
        path: str,
        *path_params: list[str],
        payload: dict[str, str],
        **kwargs,
    ):
        """
        POST data to a given path (usually to call an action)

        path:           A restconf path. Example: /ncs:devices/device/check-sync
        path_params:    Values to insert into `{}` in the URL. Values will be appropriately
                        URL encoded, so "Foo/Bar" will be encoded to "Foo%2FBar"

        Returns:        JSON Payload, or raises an exception if an error occurred
        Raises:         RestConfError or a sub-class
        """
        url = self._make_url(path, path_params)
        query_params = self.query_params(**kwargs)
        response = self.session.post(url, json=payload, params=query_params)
        self.log.info(
            "NSO Commit/Call",
            method="POST",
            url=url,
            params=query_params,
            status_code=response.status_code,
            ok=response.is_success,
            error_text=None if response.is_success else response.text,
            response_len=len(response.content),
            elapsed_time=response.elapsed.total_seconds(),
        )
        return self._parse_response(response)

    def patch(
        self,
        path: str,
        *path_params: list[str],
        payload: dict[str, str],
        style: PatchType,
        ignore_codes=(),
        **kwargs,
    ) -> PatchResult | DryRunResult:
        """
        PATCH data to a given path

        path:           A restconf path. Example: /ncs:services/pdp:pdp=PDP-1
        path_params:    Values to insert into `{}` in the URL. Values will be appropriately
                        URL encoded, so "Foo/Bar" will be encoded to "Foo%2FBar"
        payload:        JSON data
        style:          PatchType.PLAIN or PatchType.YANG_PATCH
        ignore_codes:   Defaults to empty, but can be a list of codes to not treat
                        as an error and avoid raising an exception. Typically used
                        internally for 409 errors with a YANG-Patch
        kwargs:         Query keyword arguments, see query_params()

        Returns:        JSON Payload, or raises an exception if an error occurred
        Raises:         RestConfError or a sub-class

        A PatchType.PLAIN makes this call function similar to a
        MERGE operation where existing fields are updated if they exist.
        To see an example PATCH operation, see rfc8040 section 4.6

        A PatchType.YANG_PATCH can be include a number of different operations,
        such as create/replace/merge/delete on different locations. Using the `yang_patch`
        is recommended since it takes care of a lot of boilerplate. To
        see an example YANG-Patch, see IETF draft-iet-netconf-yang-patch-14 appendix D.1.5.

        References
        - https://datatracker.ietf.org/doc/html/rfc8040#section-4.6
        - https://datatracker.ietf.org/doc/html/draft-ietf-netconf-yang-patch-14#appendix-D.1.5
        """
        url = self._make_url(path, path_params)
        query_params = self.query_params(**kwargs)

        # If using YANG-Patch, change content-type
        headers = {}
        if style == PatchType.YANG_PATCH:
            headers["Content-Type"] = ContentType.YANG_PATCH

        response = self.session.patch(
            url,
            headers=headers,
            json=payload,
            params=query_params,
        )
        self.log.info(
            "NSO Commit",
            method="PATCH",
            url=url,
            params=query_params,
            style=style,
            payload=payload,
            status_code=response.status_code,
            ok=response.is_success,
            error_text=None if response.is_success else response.text,
            response_len=len(response.content),
            elapsed_time=response.elapsed.total_seconds(),
        )
        return self._parse_response(response, ignore_codes)

    def yang_patch(self, path: str, *path_params: list[str]) -> Patch:
        """Prepare a request using the YANG-Patch.

        Example usage:
            nso = NSOClient(...)
            p = nso.yang_patch("/tailf-ncs:services/pdp:pdp={}", "MY-PDP-1")
            p.replace("/admin-state", payload={"pdp:admin-state": "in-service})
            p.delete("/lag-id")
            p.commit().raise_if_error()
        """
        return Patch(
            nso=self,
            path=path,
            path_params=path_params,
        )

    def _parse_response(
        self,
        response: httpx.Response,
        ignore_codes: list[int] = [],
    ) -> dict | DryRunResult:
        self._raise_if_error(response, ignore_codes)
        if len(response.content) == 0:
            return None
        rv = response.json()
        if DryRunResult.is_dry_run(rv):
            return DryRunResult(rv)
        return rv

    def query_params(
        self,
        **kwargs,
    ) -> dict[str, str]:
        """Generate query parameters based on kwargs passed into
        get/put/delete/post/patch calls. Note that these get merged
        with kwargs passed into NSOClient

        content: "config", "non-config", or None (default, show both)
        fields:  List[str] of fields to return (default none, show everything)
        unhide:  List[str] of groups to unhide (default, nothing)

        dry_run: "cli", "native", None (default, do not dry-run)
        no_deploy: inhibit service call actions (default no)
        """
        # Merge in defaults, preferring call parameters
        kwargs = self.commit_kwargs | kwargs

        # Generate query-string parameters to pass to requests.Request
        query_params = {}
        if "unhide" in kwargs:
            unhide = kwargs.pop("unhide")
            if unhide:
                query_params["unhide"] = ",".join()
        if "dry_run" in kwargs:
            query_params["dry-run"] = kwargs.pop("dry_run")
        if "content" in kwargs:
            query_params["content"] = kwargs.pop("content")
        if "no_deploy" in kwargs:
            kwargs.pop("no_deploy")
            query_params["no-deploy"] = ""
        if "no_networking" in kwargs:
            kwargs.pop("no_networking")
            query_params["no-networking"] = ""
        if "fields" in kwargs:
            query_params["fields"] = ";".join(kwargs.pop("fields"))

        # Pass through remaining options as-is
        for k, v in kwargs.items():
            query_params[k] = v
        return query_params

    def _make_url(self, path, args):
        """Substitute {} items in path with url encoded values"""
        url = self.nso_url + path.format(
            *[urllib.parse.quote(str(p), safe="") for p in args]
        )
        return url

    def _raise_if_error(
        self,
        response: httpx.Response,
        ignore_codes: list[int] = [],
    ) -> None:
        """Raises the appropriate exception if there is one"""

        if response.is_success:
            # no error
            return
        elif response.status_code in ignore_codes:
            # no error as defined by caller
            return
        elif response.status_code == 404:
            raise NotFoundError(response)
        elif response.status_code == 401:
            raise AccessDeniedError(response)
        elif (
            response.status_code == 400
            and "ietf-yang-patch:yang-patch-status" in response.text
        ):
            raise YangPatchError(response)
        elif response.status_code == 400:
            raise BadRequestError(response)
        else:
            # Unknown request error
            raise RestConfError(response)


class Patch:
    """A batch of operations to be submitted as a YANG PATCH"""

    nso: NSOClient
    path: str
    path_params: list[str]
    unhide: list[str]
    edits = list[dict]

    def __init__(
        self,
        nso: NSOClient,
        path: str,
        path_params: list[str] = [],
        unhide: list[str] = [],
    ):
        self.nso = nso
        self.path = path
        self.path_params = path_params
        self.unhide = []
        self.unhide.extend(unhide)
        self.edits = []

    def _format_path(self, path, args):
        """Substitute {} items in path with url encoded values

        This differs from NSOClient._format_path in that it doesn't prepend a base URL
        """
        return path.format(*[urllib.parse.quote(str(p), safe="") for p in args])

    def create(
        self,
        path: str,
        *path_params: list[str],
        value: dict[str, str],
        edit_id: str = None,
    ) -> str:
        """Create an element at a path, fail if it this path already exists
        path:        Target path to modify, may include {}
        path_params: Values to fill into {} part of the format
        value:       Value to create, note that for leaf values you will likely need to provide
                     provide a dictionary instead of just the leaf-value.
        edit_id:     Optional, specify an edit ID instead of the default

        return: Returns the edit-id
        """
        p = self._format_path(path, path_params)
        edit_id = edit_id or p
        self.edits.append(
            {
                "edit-id": edit_id,
                "operation": "create",
                "target": p,
                "value": value,
            }
        )
        return edit_id

    def delete(
        self,
        path: str,
        *path_params: list[str],
        edit_id: str = None,
    ):
        """Delete YANG data, fail if it does not exist
        path:        Target path to modify, may include {}
        path_params: Values to fill into {} part of the format
        edit_id:     Optional, specify an edit ID instead of the default

        return: Returns the edit-id
        """
        p = self._format_path(path, path_params)
        edit_id = edit_id or p
        self.edits.append(
            {
                "edit-id": edit_id,
                "operation": "delete",
                "target": p,
            }
        )
        return edit_id

    def insert(
        self,
        path: str,
        *path_params: list[str],
        where: InsertWhere,
        point: str = None,
        value: dict[str, str],
        edit_id: str = None,
    ):
        """Create an element at a path, inserting before/after an existing element. Only valid for user-ordered items

        path:        Target path to modify, may include {}
        path_params: Values to fill into {} part of the format
        point:       insert relative-to (needed if using BEFORE/AFTER)
        where:       FIRST/LAST/BEFORE/AFTER
        value:       Value to create, note that for leaf values you will likely need to provide
                     provide a dictionary instead of just the leaf-value.
        edit_id:     Optional, specify an edit ID instead of the default

        return: Returns the edit-id
        """
        p = self._format_path(path, path_params)
        edit_id = edit_id or p
        op = {
            "edit-id": edit_id,
            "operation": "insert",
            "target": p,
            "where": where.value,
            "value": value,
        }
        if where in (InsertWhere.BEFORE, InsertWhere.AFTER):
            op["point"] = point

        self.edits.append(op)
        return edit_id

    def merge(
        self,
        path: str,
        *path_params: list[str],
        value: dict[str, str],
        edit_id: str = None,
    ):
        """Merge data into an existing path

        path:        Target path to modify, may include {}
        path_params: Values to fill into {} part of the format
        value:       Value(s) to merge in, note that for leaf values you will likely need to provide
                     provide a dictionary instead of just the leaf-value.
        edit_id:     Optional, specify an edit ID instead of the default

        return: Returns the edit-id
        """
        p = self._format_path(path, path_params)
        edit_id = edit_id or p
        self.edits.append(
            {
                "edit-id": edit_id,
                "operation": "merge",
                "target": p,
                "value": value,
            }
        )
        return edit_id

    def move(
        self,
        path: str,
        *path_params: list[str],
        where: InsertWhere,
        point: str = None,
        edit_id: str = None,
    ):
        """Move an existing element, only valid for user-ordered lists

        path:        Target path to modify, may include {}
        path_params: Values to fill into {} part of the format
        point:       insert relative-to (needed if using BEFORE/AFTER)
        where:       FIRST/LAST/BEFORE/AFTERlikely need to provide
                     provide a dictionary instead of just the leaf-value.
        edit_id:     Optional, specify an edit ID instead of the default

        return: Returns the edit-id
        """
        p = self._format_path(path, path_params)
        edit_id = edit_id or p
        op = {
            "edit-id": edit_id,
            "operation": "move",
            "target": p,
            "where": where.value,
        }
        if where in (InsertWhere.BEFORE, InsertWhere.AFTER):
            op["point"] = point

        self.edits.append(op)
        return edit_id

    def replace(
        self,
        path: str,
        *path_params: list[str],
        value: dict[str, str],
        edit_id: str = None,
    ):
        pass

        """Delete YANG data, succeed if it's already gone
        path:        Target path to modify, may include {}
        path_params: Values to fill into {} part of the format
        edit_id:     Optional, specify an edit ID instead of the default

        return: Returns the edit-id
        """
        p = self._format_path(path, path_params)
        edit_id = edit_id or p
        self.edits.append(
            {
                "edit-id": edit_id,
                "operation": "replace",
                "target": p,
                "value": value,
            }
        )
        return edit_id

    def commit(
        self,
        patch_id: str = None,
        comment: str = None,
        **kwargs,
    ) -> PatchResult | DryRunResult:
        """Execute the prepared patch. Patch is executed atomically

        patch_id: Specify patch-id (not needed)
        comment:  Optional, Comment to pass to the RestConf server
        kwargs:         Query keyword arguments, see query_params()
        """
        payload = {
            "patch-id": patch_id or self.path,
            "edit": self.edits,
        }
        if comment:
            payload["comment"] = comment
        resp = self.nso.patch(
            self.path,
            *self.path_params,
            payload={"ietf-yang-patch:yang-patch": payload},
            style=PatchType.YANG_PATCH,
            unhide=self.unhide,
            ignore_codes=(409,),
            **kwargs,
        )

        # Dry-run response
        if isinstance(resp, DryRunResult):
            return resp

        # Standard response
        elif "ietf-yang-patch:yang-patch-status" in resp:
            resp = resp["ietf-yang-patch:yang-patch-status"]
            edits = resp.get("edit-status", {}).get("edits", [])
            return PatchResult(
                patch_id=resp["patch-id"],
                edits={e["edit-id"] for e in edits},
                ok=("ok" in resp),
            )
        else:
            raise NotImplementedError(
                f"Unable to detect response format; keys={list(resp.keys())}"
            )


@dataclass
class PatchResult:
    """Result of a Patch operation"""

    patch_id: str
    edits: dict[str, dict]
    ok: bool

    def raise_if_error(self):
        if not self.ok:
            raise PatchError(self)


class DryRunResult:
    """
    result.dry_run # => DryRunType.CLI
    result.changes # => {"local-node": "..."}
    """

    class DryRunType(Enum):
        CLI = "cli"
        XML = "xml"
        NATIVE = "NATIVE"

    dry_run: DryRunType
    changes: dict[str, str] | None  # "local-node" -> "data"

    def __init__(self, response: dict[str, any]):
        """Construct a response from a RestConf response"""
        response = response["dry-run-result"]
        changes = {}
        if "cli" in response:
            self.dry_run = self.DryRunType.CLI
            changes = response["cli"]
        elif "result-xml" in response:
            self.dry_run = self.DryRunType.XML
            changes = response["result-xml"]
        elif "native" in response:
            self.dry_run = self.DryRunType.CLI
            changes = response["native"]
        else:
            raise NotImplementedError(
                f"Not sure how to interpret dry-run with keys {list(response.keys())}"
            )

        # Simplify the changes structure
        self.changes = {k: v["data"] for k, v in changes.items()}

    def __str__(self) -> str:
        if self.changes == {}:
            return ""
        # elif tuple(self.changes.keys()) == ("local-node",):
        #     return self.changes["local-node"]
        else:
            return "\n".join([f"{node}: {data}" for node, data in self.changes.items()])

    @classmethod
    def is_dry_run(cls, response) -> bool:
        return "dry-run-result" in response
