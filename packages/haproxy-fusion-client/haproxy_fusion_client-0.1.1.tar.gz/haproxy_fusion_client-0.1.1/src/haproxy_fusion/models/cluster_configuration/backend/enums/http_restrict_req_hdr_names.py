from enum import Enum


class HttpRestrictReqHdrNames(str, Enum):
    PRESERVE = "preserve"
    DELETE = "delete"
    REJECT = "reject"