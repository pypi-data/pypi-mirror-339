from enum import Enum


class LogFormat(str, Enum):
    LOCAL = "local"
    RFC3164 = "rfc3164"
    RFC5424 = "rfc5424"
    PRIORITY = "priority"
    SHORT = "short"
    TIMED = "timed"
    ISO = "iso"
    RAW = "raw"
