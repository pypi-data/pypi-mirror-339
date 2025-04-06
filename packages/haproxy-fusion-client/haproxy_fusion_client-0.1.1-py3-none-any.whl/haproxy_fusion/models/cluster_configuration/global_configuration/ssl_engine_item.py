from haproxy_fusion.models.base.base_model import BaseModel


class SSLEngineItem(BaseModel):
    name: str
    algorithms: str | None = None