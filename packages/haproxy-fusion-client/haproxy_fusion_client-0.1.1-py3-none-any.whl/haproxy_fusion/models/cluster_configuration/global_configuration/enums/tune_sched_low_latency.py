from enum import Enum


class TuneSchedLowLatency(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
