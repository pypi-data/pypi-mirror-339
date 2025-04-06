from enum import Enum


class SslModeAsync(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
