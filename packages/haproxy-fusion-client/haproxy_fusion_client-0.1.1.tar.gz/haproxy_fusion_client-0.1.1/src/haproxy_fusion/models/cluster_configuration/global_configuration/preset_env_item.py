from haproxy_fusion.models.base.base_model import BaseModel


class PresetEnvItem(BaseModel):
    name: str
    value: str