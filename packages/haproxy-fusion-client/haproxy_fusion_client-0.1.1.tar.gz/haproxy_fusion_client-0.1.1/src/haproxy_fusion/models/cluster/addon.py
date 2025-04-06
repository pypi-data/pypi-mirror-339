from haproxy_fusion.models.base.base_model import BaseModel


class Addon(BaseModel):
    addon_name: str | None = None
    addon_enabled: bool | None = None
