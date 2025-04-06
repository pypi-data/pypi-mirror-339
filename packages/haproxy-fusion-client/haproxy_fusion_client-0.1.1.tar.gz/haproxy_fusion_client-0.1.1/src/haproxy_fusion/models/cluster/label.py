from haproxy_fusion.models.base.base_model import BaseModel


class Label(BaseModel):
    key: str
    value: str | None = None
