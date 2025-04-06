from enum import Enum


class SeverityOutput(str, Enum):
    NONE = "none"
    NUMBER = "number"
    STRING = "string"
