from enum import Enum


class BalanceAlgorithm(str, Enum):
    roundrobin = "roundrobin"
    static_rr = "static-rr"
    leastconn = "leastconn"
    first = "first"
    source = "source"
    uri = "uri"
    url_param = "url_param"
    hdr = "hdr"
    random = "random"
    rdp_cookie = "rdp-cookie"
    hash_ = "hash"