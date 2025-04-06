from haproxy_fusion.models.base.base_model import BaseModel


class MaxmindDB(BaseModel):
    name: str | None = None
    path: str | None = None