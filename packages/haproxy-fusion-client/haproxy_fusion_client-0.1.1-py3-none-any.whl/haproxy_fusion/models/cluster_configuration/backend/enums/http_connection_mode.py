from enum import Enum


class HttpConnectionMode(Enum):
    HTTP_CLOSE = "httpclose"
    HTTP_SERVER_CLOSE = "http-server-close"
    HTTP_KEEP_ALIVE = "http-keep-alive"