from enum import Enum


class LoadServerState(str, Enum):
    GLOBAL = "global_configuration"
    LOCAL = "local"
    NONE = "none"
