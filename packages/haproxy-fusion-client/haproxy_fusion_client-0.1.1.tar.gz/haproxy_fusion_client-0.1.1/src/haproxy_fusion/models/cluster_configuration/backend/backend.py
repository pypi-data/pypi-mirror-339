from pydantic import Field

from haproxy_fusion.models.base.base_model import BaseModel
from haproxy_fusion.models.cluster_configuration.backend.balance import Balance
from haproxy_fusion.models.cluster_configuration.backend.enums.adv_check import AdvCheck
from haproxy_fusion.models.cluster_configuration.backend.enums.http_connection_mode import HttpConnectionMode
from haproxy_fusion.models.cluster_configuration.backend.enums.http_restrict_req_hdr_names import \
    HttpRestrictReqHdrNames
from haproxy_fusion.models.cluster_configuration.backend.enums.http_reuse import HttpReuse
from haproxy_fusion.models.cluster_configuration.backend.enums.load_server_state_from_file import \
    LoadServerStateFromFile
from haproxy_fusion.models.cluster_configuration.backend.enums.mode import Mode
from haproxy_fusion.models.cluster_configuration.enums.enabled_disabled import EnabledDisabled


class Backend(BaseModel):
    abortonclose: EnabledDisabled | None = None
    accept_invalid_http_response: EnabledDisabled | None = None
    adv_check: AdvCheck | None = None
    allbackups: EnabledDisabled | None = None
    balance: Balance | None = None
    bind_process: str | None = Field(None, pattern=r"^\S+$")
    check_timeout: int | None = None
    checkcache: EnabledDisabled | None = None
    compression: dict | None = None
    connect_timeout: int | None = None
    cookie: dict | None = None
    default_server: dict | None = None
    description: str | None = None
    disabled: bool | None = None
    dynamic_cookie_key: str | None = Field(None, pattern=r"^\S+$")
    email_alert: dict | None = None
    enabled: bool | None = None
    error_files: list | None = None
    errorfiles_from_http_errors: list | None = None
    errorloc302: dict | None = None
    errorloc303: dict | None = None
    external_check: EnabledDisabled | None = None
    external_check_command: str | None = Field(None, pattern=r"^\S+$")
    external_check_path: str | None = Field(None, pattern=r"^\S+$")
    force_persist: dict | None = None
    forwardfor: dict | None = None
    from_: str | None = Field(None, alias="from", pattern=r"^[A-Za-z0-9\-_.:]+$")
    fullconn: int | None = None
    h1_case_adjust_bogus_server: EnabledDisabled | None = None
    hash_type: dict | None = None
    http_buffer_request: EnabledDisabled | None = Field(None, alias="http-buffer-request")
    http_check: dict | None = Field(None, alias="http-check")
    http_keep_alive: EnabledDisabled | None = Field(None, alias="http-keep-alive")
    http_no_delay: EnabledDisabled | None = Field(None, alias="http-no-delay")
    http_server_close: EnabledDisabled | None = Field(None, alias="http-server-close")
    http_use_htx: EnabledDisabled | None = Field(None, alias="http-use-htx", pattern=r"^\S+$")
    http_connection_mode: HttpConnectionMode | None = None
    http_keep_alive_timeout: int | None = None
    http_pretend_keepalive: EnabledDisabled | None = None
    http_proxy: EnabledDisabled | None = None
    http_request_timeout: int | None = None
    http_restrict_req_hdr_names: HttpRestrictReqHdrNames | None = None
    http_reuse: HttpReuse | None = None
    http_send_name_header: str | None = None
    httpchk_params: dict | None = None
    httpclose: EnabledDisabled | None = None
    id: int | None = None
    ignore_persist: dict | None = None
    independent_streams: EnabledDisabled | None = None
    load_server_state_from_file: LoadServerStateFromFile | None = None
    log_health_checks: EnabledDisabled | None = None
    log_tag: str | None = Field(None, pattern=r"^\S+$")
    max_keep_alive_queue: int | None = None
    mode: Mode | None = None
    mysql_check_params: dict | None = None
    name: str = Field(..., pattern=r"^[A-Za-z0-9\-_.:]+$")
    nolinger: EnabledDisabled | None = None
    originalto: dict | None = None
    persist: EnabledDisabled | None = None
    persist_rule: dict | None = None
    pgsql_check_params: dict | None = None
    prefer_last_server: EnabledDisabled | None = None
    queue_timeout: int | None = None
    redispatch: dict | None = None
    retries: int | None = None
    retry_on: str | None = None
    server_fin_timeout: int | None = None
    server_state_file_name: str | None = None
    server_timeout: int | None = None
    smtpchk_params: dict | None = None
    source: dict | None = None
    splice_auto: EnabledDisabled | None = None
    splice_request: EnabledDisabled | None = None
    splice_response: EnabledDisabled | None = None
    spop_check: EnabledDisabled | None = None
    srvtcpka: EnabledDisabled | None = None
    srvtcpka_cnt: int | None = None
    srvtcpka_idle: int | None = None
    srvtcpka_intvl: int | None = None
    stats_options: dict | None = None
    stick_table: dict | None = None
    tarpit_timeout: int | None = None
    tcp_smart_connect: EnabledDisabled | None = None
    tcpka: EnabledDisabled | None = None
    transparent: EnabledDisabled | None = None
    tunnel_timeout: int | None = None
    use_fcgi_app: str | None = None
    acls: list | None = None
    filters: list | None = None
    http_after_response_rules: list | None = None
    http_checks: list | None = None
    http_error_rules: list | None = None
    http_request_rules: list | None = None
    http_response_rules: list | None = None
    log_targets: list | None = None
    server_switching_rules: list | None = None
    server_templates: list | None = None
    servers: list | None = None
    stick_rules: list | None = None
    tcp_check_rules: list | None = None
    tcp_request_rules: list | None = None
    tcp_response_rules: list | None = None
    waf_body_rules: list | None = None
