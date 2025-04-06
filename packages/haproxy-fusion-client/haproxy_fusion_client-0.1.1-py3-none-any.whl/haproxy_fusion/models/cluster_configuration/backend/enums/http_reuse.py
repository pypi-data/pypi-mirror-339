from enum import Enum


class HttpReuse(Enum):
    AGGRESSIVE = "aggressive"
    ALWAYS = "always"
    NEVER = "never"
    SAFE = "safe"
