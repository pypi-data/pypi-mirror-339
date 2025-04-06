from haproxy_fusion.models.base.base_model import BaseModel


class SetVarItem(BaseModel):
    expr: str
    name: str