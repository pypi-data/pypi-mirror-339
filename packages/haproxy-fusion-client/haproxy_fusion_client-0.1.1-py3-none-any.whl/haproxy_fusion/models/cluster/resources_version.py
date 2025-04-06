from haproxy_fusion.models.base.base_model import BaseModel


class ResourcesVersion(BaseModel):
    configuration: int | None = None
    disk_storage: int | None = None
    global_version: int | None = None
    id: str | None = None
    timestamp: str | None = None
    vrrp: int | None = None
    waf: int | None = None
