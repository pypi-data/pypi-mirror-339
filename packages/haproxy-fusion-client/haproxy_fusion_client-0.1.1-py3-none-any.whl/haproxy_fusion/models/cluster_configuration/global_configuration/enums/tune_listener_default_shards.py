from enum import Enum


class TuneListenerDefaultShards(str, Enum):
    BY_PROCESS = "by-process"
    BY_THREAD = "by-thread"
    BY_GROUP = "by-group"
