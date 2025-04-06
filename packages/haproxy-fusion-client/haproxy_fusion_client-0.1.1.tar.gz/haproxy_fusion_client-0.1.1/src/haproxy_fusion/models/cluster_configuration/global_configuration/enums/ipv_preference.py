from enum import Enum


class IPvPreference(str, Enum):
    IPV4 = "ipv4"
    IPV6 = "ipv6"