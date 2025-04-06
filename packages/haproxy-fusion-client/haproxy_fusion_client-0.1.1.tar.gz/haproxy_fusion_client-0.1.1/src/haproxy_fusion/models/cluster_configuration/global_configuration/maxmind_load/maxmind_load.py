from haproxy_fusion.models.base.base_model import BaseModel
from haproxy_fusion.models.cluster_configuration.global_configuration.maxmind_load.maxmind_db import MaxmindDB


class MaxmindLoad(BaseModel):
    maxmind_dbs: list[MaxmindDB] | None = None
    mlock_max: int | None = None
