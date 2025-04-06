from pydantic import Field

from haproxy_fusion.models.base.base_model import BaseModel
from haproxy_fusion.models.cluster.addon import Addon
from haproxy_fusion.models.cluster.label import Label
from haproxy_fusion.models.cluster.resources_version import ResourcesVersion


class Cluster(BaseModel):
    id: str
    name: str
    configuration_id: str
    storage_dir: str
    version: int = Field(alias="_version")

    bootstrap_key_duration: int | None = None
    addons: list[Addon] | None = None
    auto_join: bool | None = None
    bootstrap_key: str | None = None
    bootstrap_key_expiring_date: str | None = None
    ca_certificate: str | None = None
    ca_certificate_priv_key: str | None = None
    certificate: str | None = None
    certificate_priv_key: str | None = None
    cluster_global_section: str | None = None
    cluster_group: str | None = None
    configuration_version: int | None = None
    description: str | None = None
    forward_haproxy_logs: bool | None = None
    gpe_port: int | None = None
    hapee_license: str | None = None
    haproxy_binary: str | None = None
    haproxy_modules: str | None = None
    labels: list[Label] | None = None
    log_target: int | None = None
    max_snapshots: int | None = None
    min_snapshots: int | None = None
    namespace: str | None = None
    network_configuration: str | None = None
    node_auto_renew_before_expire: int | None = None
    node_certificate_duration: int | None = None
    node_timeout: int | None = None
    relaxed_node_joining: bool | None = None
    resources_version: ResourcesVersion | None = None
    skip_reload: bool | None = None
    snapshots_expiration: int | None = None
    success_policy: float | None = None
