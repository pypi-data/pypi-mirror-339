from pydantic import Field

from haproxy_fusion.models.base.base_model import BaseModel
from haproxy_fusion.models.cluster_configuration.enums.enabled_disabled import EnabledDisabled


class LogSendHostname(BaseModel):
    enabled: EnabledDisabled
    param: str | None = Field(None, pattern=r'^\S+$')
