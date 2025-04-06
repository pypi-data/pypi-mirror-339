from enum import Enum


class NumaCpuMapping(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
