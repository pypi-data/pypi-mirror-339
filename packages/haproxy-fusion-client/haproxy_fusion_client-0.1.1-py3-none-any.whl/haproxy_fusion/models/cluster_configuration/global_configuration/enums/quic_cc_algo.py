from enum import Enum


class QuicCcAlgo(str, Enum):
    CUBIC = "cubic"
    NEWRENO = "newreno"
