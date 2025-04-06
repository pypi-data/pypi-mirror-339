from enum import Enum


class HttpClientSslVerify(str, Enum):
    EMPTY = ""
    NONE = "none"
    REQUIRED = "required"