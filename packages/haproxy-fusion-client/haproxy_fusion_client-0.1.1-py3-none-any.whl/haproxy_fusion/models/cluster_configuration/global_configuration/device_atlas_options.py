from haproxy_fusion.models.base.base_model import BaseModel


class DeviceAtlasOptions(BaseModel):
    json_file: str | None = None
    log_level: str | None = None
    properties_cookie: str | None = None
    separator: str | None = None
