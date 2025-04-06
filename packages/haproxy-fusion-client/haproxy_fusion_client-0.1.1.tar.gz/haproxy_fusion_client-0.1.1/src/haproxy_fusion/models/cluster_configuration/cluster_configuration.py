from pydantic import Field

from haproxy_fusion.models.base.base_model import BaseModel
from haproxy_fusion.models.cluster_configuration.backend.backend import Backend
from haproxy_fusion.models.cluster_configuration.global_configuration.global_configuration import \
    GlobalConfiguration


class ClusterConfiguration(BaseModel):
    backends: list[Backend] | None = None
    caches: list[dict] | None = None
    dynamic_update: dict | None = None
    fcgi_apps: list[dict] | None = None
    frontends: list[dict] | None = None
    global_: GlobalConfiguration | None = Field(None, alias="global")
    http_errors: list[dict] | None = None
    log_forwards: list[dict] | None = None
    mailers_sections: list[dict] | None = None
    named_defaults: list[dict] | None = None
    peers: list[dict] | None = None
    programs: list[dict] | None = None
    resolvers: list[dict] | None = None
    rings: list[dict] | None = None
    userlists: list[dict] | None = None
