from pydantic import Field

from haproxy_fusion.models.base.base_model import BaseModel
from haproxy_fusion.models.cluster_configuration.backend.enums.balance_algorithm import BalanceAlgorithm


class Balance(BaseModel):
    algorithm: BalanceAlgorithm
    hash_expression: str | None = None
    hdr_name: str | None = None
    hdr_use_domain_only: bool | None = None
    random_draws: int | None = None
    rdp_cookie_name: str | None = Field(None, pattern=r"^\S+$")
    uri_depth: int | None = None
    uri_len: int | None = None
    uri_path_only: bool | None = None
    uri_whole: bool | None = None
    url_param: str | None = Field(None, pattern=r"^\S+$")
    url_param_check_post: int | None = None
    url_param_max_wait: int | None = None
