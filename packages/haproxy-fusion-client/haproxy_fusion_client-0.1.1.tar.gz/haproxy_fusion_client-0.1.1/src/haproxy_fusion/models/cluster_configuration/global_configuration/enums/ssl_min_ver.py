from enum import Enum


class SslMinVer(str, Enum):
    SSLV3 = "SSLv3"
    TLSV10 = "TLSv1.0"
    TLSV11 = "TLSv1.1"
    TLSV12 = "TLSv1.2"
    TLSV13 = "TLSv1.3"
