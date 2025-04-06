from enum import Enum


class SslServerVerify(str, Enum):
    NONE = "none"
    REQUIRED = "required"
