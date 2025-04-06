from haproxy_fusion.models.base.base_model import BaseModel


class CpuMap(BaseModel):
    cpu_set: str
    process: str
