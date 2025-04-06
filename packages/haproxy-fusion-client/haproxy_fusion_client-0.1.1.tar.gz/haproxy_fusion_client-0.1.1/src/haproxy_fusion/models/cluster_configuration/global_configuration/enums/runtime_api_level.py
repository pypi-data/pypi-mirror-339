from enum import Enum


class RuntimeApiLevel(str, Enum):
    USER = "user"
    OPERATOR = "operator"
    ADMIN = "admin"
