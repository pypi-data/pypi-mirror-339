from haproxy_fusion.models.base.base_model import BaseModel


class SetVarFmtItem(BaseModel):
    format: str
    name: str
