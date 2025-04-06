from pydantic import Field

from haproxy_fusion.models.base.base_model import BaseModel
from haproxy_fusion.models.cluster_configuration.enums.enabled_disabled import EnabledDisabled
from haproxy_fusion.models.cluster_configuration.global_configuration.cpu_map import CpuMap
from haproxy_fusion.models.cluster_configuration.global_configuration.default_path import DefaultPath
from haproxy_fusion.models.cluster_configuration.global_configuration.device_atlas_options import DeviceAtlasOptions
from haproxy_fusion.models.cluster_configuration.global_configuration.enums.http_client_ssl_verify import \
    HttpClientSslVerify
from haproxy_fusion.models.cluster_configuration.global_configuration.enums.ipv_preference import IPvPreference
from haproxy_fusion.models.cluster_configuration.global_configuration.enums.load_server_state import LoadServerState
from haproxy_fusion.models.cluster_configuration.global_configuration.enums.numa_cpu_mapping import NumaCpuMapping
from haproxy_fusion.models.cluster_configuration.global_configuration.enums.profiling_tasks import ProfilingTasks
from haproxy_fusion.models.cluster_configuration.global_configuration.enums.ssl_mode_async import SslModeAsync
from haproxy_fusion.models.cluster_configuration.global_configuration.enums.ssl_server_verify import SslServerVerify
from haproxy_fusion.models.cluster_configuration.global_configuration.fifty_one_degrees_options import \
    FiftyOneDegreesOptions
from haproxy_fusion.models.cluster_configuration.global_configuration.h1_case_adjust_item import H1CaseAdjustItem
from haproxy_fusion.models.cluster_configuration.global_configuration.log_send_hostname import LogSendHostname
from haproxy_fusion.models.cluster_configuration.global_configuration.log_target import LogTarget
from haproxy_fusion.models.cluster_configuration.global_configuration.lua_load import LuaLoad
from haproxy_fusion.models.cluster_configuration.global_configuration.lua_prepend_path import LuaPrependPath
from haproxy_fusion.models.cluster_configuration.global_configuration.maxmind_load.maxmind_load import MaxmindLoad
from haproxy_fusion.models.cluster_configuration.global_configuration.maxmind_update import MaxmindUpdate
from haproxy_fusion.models.cluster_configuration.global_configuration.module_load_item import ModuleLoadItem
from haproxy_fusion.models.cluster_configuration.global_configuration.preset_env_item import PresetEnvItem
from haproxy_fusion.models.cluster_configuration.global_configuration.runtime_api import RuntimeAPI
from haproxy_fusion.models.cluster_configuration.global_configuration.set_var_fmt_item import SetVarFmtItem
from haproxy_fusion.models.cluster_configuration.global_configuration.set_var_item import SetVarItem
from haproxy_fusion.models.cluster_configuration.global_configuration.ssl_engine_item import SSLEngineItem
from haproxy_fusion.models.cluster_configuration.global_configuration.tune_options import TuneOptions


class GlobalConfiguration(BaseModel):
    anonkey: int | None = Field(None, ge=0, le=4294967295)
    busy_polling: bool | None = None
    ca_base: str | None = None
    chroot: str | None = Field(None, pattern=r'^\S+$')
    close_spread_time: int | None = None
    cluster_secret: str | None = None

    cpu_maps: list[CpuMap] | None = None
    crt_base: str | None = None
    daemon: EnabledDisabled | None = None

    default_path: DefaultPath | None = None
    description: str | None = None
    device_atlas_options: DeviceAtlasOptions | None = None
    external_check: bool | None = None
    expose_experimental_directives: bool | None = None

    fifty_one_degrees_options: FiftyOneDegreesOptions | None = None
    fingerprint_ssl_bufsize: int | None = None
    gid: int | None = None
    grace: int | None = None
    group: str | None = Field(None, pattern=r'^\S+$')

    h1_case_adjust: list[H1CaseAdjustItem] | None = None
    h1_case_adjust_file: str | None = None
    h2_workaround_bogus_websocket_clients: bool | None = None
    hard_stop_after: int | None = None

    httpclient_resolvers_disabled: EnabledDisabled | None = None
    httpclient_resolvers_id: str | None = None
    httpclient_resolvers_prefer: IPvPreference | None = None
    httpclient_retries: int | None = None
    httpclient_ssl_ca_file: str | None = None
    httpclient_ssl_verify: HttpClientSslVerify | None = None
    httpclient_timeout_connect: int | None = None

    insecure_fork_wanted: bool | None = None
    insecure_setuid_wanted: bool | None = None
    issuers_chain_path: str | None = None
    load_server_state_from_file: LoadServerState | None = None
    localpeer: str | None = Field(None, pattern=r'^\S+$')
    log_send_hostname: LogSendHostname | None = None

    lua_load_per_thread: str | None = None
    lua_loads: list[LuaLoad] | None = None
    lua_prepend_path: list[LuaPrependPath] | None = None

    master_worker: bool | None = Field(None, alias="master-worker")
    max_spread_checks: int | None = None
    maxcompcpuusage: int | None = None
    maxcomprate: int | None = None
    maxconn: int | None = None
    maxconnrate: int | None = None

    maxmind_cache_size: int | None = None
    maxmind_debug: bool | None = None
    maxmind_load: MaxmindLoad | None = None
    maxmind_update: MaxmindUpdate | None = None

    maxpipes: int | None = None
    maxsessrate: int | None = None
    maxsslconn: int | None = None
    maxsslrate: int | None = None
    maxzlibmem: int | None = None

    modsecurity_deny_blocking_io: bool | None = Field(None, alias="modsecurity-deny-blocking-io")
    module_loads: list[ModuleLoadItem] | None = Field(None, alias="module-loads")
    module_path: str | None = Field(None, alias="module-path")

    mworker_max_reloads: int | None = None
    nbproc: int | None = None
    nbthread: int | None = None
    no_quic: bool | None = None
    node: str | None = None
    noepoll: bool | None = None
    noevports: bool | None = None
    nogetaddrinfo: bool | None = None
    nokqueue: bool | None = None
    nopoll: bool | None = None
    noreuseport: bool | None = None
    nosplice: bool | None = None

    numa_cpu_mapping: NumaCpuMapping | None = None
    pidfile: str | None = None
    pp2_never_send_local: bool | None = None
    prealloc_fd: bool | None = Field(None, alias="prealloc-fd")
    presetenv: list[PresetEnvItem] | None = None
    profiling_tasks: ProfilingTasks | None = None
    quiet: bool | None = None
    resetenv: str | None = None

    runtime_apis: list[RuntimeAPI] | None = None
    server_state_base: str | None = Field(None, pattern=r'^\S+$')
    server_state_file: str | None = Field(None, pattern=r'^\S+$')
    set_dumpable: bool | None = None
    set_var: list[SetVarItem] | None = None
    set_var_fmt: list[SetVarFmtItem] | None = None
    setenv: list[PresetEnvItem] | None = None

    spread_checks: int | None = None
    ssl_default_bind_ciphers: str | None = None
    ssl_default_bind_ciphersuites: str | None = None
    ssl_default_bind_client_sigalgs: str | None = None
    ssl_default_bind_curves: str | None = None
    ssl_default_bind_options: str | None = None
    ssl_default_bind_sigalgs: str | None = None
    ssl_default_server_ciphers: str | None = None
    ssl_default_server_ciphersuites: str | None = None
    ssl_default_server_client_sigalgs: str | None = None
    ssl_default_server_curves: str | None = None
    ssl_default_server_options: str | None = None
    ssl_default_server_sigalgs: str | None = None
    ssl_dh_param_file: str | None = None
    ssl_engines: list[SSLEngineItem] | None = None
    ssl_load_extra_files: str | None = None
    ssl_mode_async: SslModeAsync | None = None
    ssl_server_verify: SslServerVerify | None = None
    ssl_skip_self_issued_ca: bool | None = None

    stats_maxconn: int | None = None
    stats_timeout: int | None = None
    strict_limits: bool | None = None
    thread_group_lines: list[dict] | None = None
    thread_groups: int | None = None

    tune_options: TuneOptions | None = None
    tune_ssl_default_dh_param: int | None = None

    uid: int | None = None
    ulimit_n: int | None = None
    unsetenv: str | None = None
    user: str | None = Field(None, pattern=r'^\S+$')

    waf_body_limit: int | None = Field(None, alias="waf-body-limit")
    waf_json_levels: int | None = Field(None, alias="waf-json-levels")
    waf_load: str | None = Field(None, alias="waf-load")

    wurfl_options: dict | None = None

    log_targets: list[LogTarget] | None = None
