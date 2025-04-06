from pydantic import Field

from haproxy_fusion.models.base.base_model import BaseModel
from haproxy_fusion.models.cluster_configuration.global_configuration.enums.log_format import LogFormat
from haproxy_fusion.models.cluster_configuration.global_configuration.enums.log_level import LogLevel
from haproxy_fusion.models.cluster_configuration.global_configuration.enums.syslog_facility import SyslogFacility


class LogTarget(BaseModel):
    index: int | None = None
    address: str | None = Field(None, pattern=r'^\S+$')
    facility: SyslogFacility | None = None
    format: LogFormat | None = None
    global_: bool | None = Field(None, alias="global_configuration")
    length: int | None = None
    level: LogLevel | None = None
    minlevel: LogLevel | None = None
    nolog: bool | None = None
    sample_range: str | None = None
    sample_size: int | None = None