from enum import Enum


class TuneIdlePoolShared(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
