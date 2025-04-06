from enum import Enum


class TuneSslKeylog(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
