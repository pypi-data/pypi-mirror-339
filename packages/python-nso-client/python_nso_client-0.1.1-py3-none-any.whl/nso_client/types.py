from enum import Enum


class ContentType(str, Enum):
    YANG_DATA = "application/yang-data+json"
    YANG_PATCH = "application/yang-patch+json"


class PatchType(str, Enum):
    PLAIN = "plain"
    YANG_PATCH = "yang-patch"


class InsertWhere(str, Enum):
    FIRST = "first"
    LAST = "last"
    BEFORE = "before"
    AFTER = "after"
