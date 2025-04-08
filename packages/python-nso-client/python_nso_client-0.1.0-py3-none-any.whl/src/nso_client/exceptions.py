import json

import httpx
import structlog


# Response errors
class RestConfError(Exception):
    """General RestConf Error

    error_type, error_tag, and error_message fields will be parsed
    if at all possible

    Protocol Reference:
     - https://github.com/YangModels/yang/blob/main/standard/ietf/RFC/ietf-restconf%402017-01-26.yang#L126-L203
    """

    error_type: str = None
    error_tag: str = None
    error_message: str = None
    response: httpx.Response

    def __init__(self, response: httpx.Response):
        super().__init__()
        logger = structlog.get_logger().bind(
            response_text=response.text,
            response_code=response.status_code,
        )

        self.response = response
        try:
            response_json: dict[str, any] = response.json()

            if yp_err := response_json.get("ietf-yang-patch:yang-patch-status", None):
                # YangPatch error
                edits = yp_err["edit-status"]["edit"]
                err = edits[0]["errors"]["error"][0]
                self.error_type = err["error-tag"]
                self.error_message = err["error-message"]

            elif rc_err := response_json.get("ietf-restconf:errors", None):
                # General restconf error
                err = rc_err["error"][0]
                self.error_type = err["error-type"]
                self.tag = err["error-tag"]
                self.error_message = err.get("error-message", None)

            else:
                # Other un-recognized error
                logger.error("Could not interpret error from NSO")
                self.error_type = "unknown-error"
                self.error_message = response.text

        except (KeyError, IndexError, json.JSONDecodeError) as e:
            # Likely caused by the response error not being an error
            logger.exception(
                "Problem interpreting RestConfError",
                exception=e,
            )
            self.error_type = "unknown-error"
            self.error_message = response.text

    def __str__(self) -> str:
        # Note, we may want to consider including these in the future
        #  self.response.url
        #  self.response.request.body
        return f"{self.error_type}: {self.error_message}"


class NotFoundError(RestConfError):
    """Path syntax is valid, but no object present at path (404)"""

    pass


class AccessDeniedError(RestConfError):
    """Authentication information is invalid or not authorized to access resource (401)"""

    pass


class YangPatchError(RestConfError):
    """YangPatch failed (400)"""

    pass


class BadRequestError(RestConfError):
    """General error with a request (400)"""


class PatchError(Exception):
    pass
