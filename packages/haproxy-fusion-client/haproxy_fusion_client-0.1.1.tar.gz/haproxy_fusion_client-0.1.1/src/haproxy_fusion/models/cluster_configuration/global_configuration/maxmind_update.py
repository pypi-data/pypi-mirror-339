from haproxy_fusion.models.base.base_model import BaseModel


class MaxmindUpdate(BaseModel):
    checksum: bool | None = None
    delay: int | None = None
    dontlog_normal: bool | None = None
    hash: bool | None = None
    log: bool | None = None
    maxmind_urls: list[dict] | None = None
    retries: int | None = None
    timeout: int | None = None
