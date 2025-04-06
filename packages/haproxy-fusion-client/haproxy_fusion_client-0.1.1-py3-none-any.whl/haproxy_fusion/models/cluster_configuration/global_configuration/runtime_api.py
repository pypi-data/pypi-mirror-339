from pydantic import Field

from haproxy_fusion.models.base.base_model import BaseModel
from haproxy_fusion.models.cluster_configuration.global_configuration.enums.quic_cc_algo import QuicCcAlgo
from haproxy_fusion.models.cluster_configuration.global_configuration.enums.runtime_api_level import RuntimeApiLevel
from haproxy_fusion.models.cluster_configuration.global_configuration.enums.severity_output import SeverityOutput
from haproxy_fusion.models.cluster_configuration.global_configuration.enums.ssl_max_ver import SslMaxVer
from haproxy_fusion.models.cluster_configuration.global_configuration.enums.ssl_min_ver import SslMinVer


class RuntimeAPI(BaseModel):
    address: str = Field(pattern=r'^\S+$')
    accept_netscaler_cip: int | None = None
    accept_proxy: bool | None = None
    allow_0rtt: bool | None = None
    alpn: str | None = Field(None, pattern=r'^\S+$')
    backlog: str | None = None
    ca_ignore_err: str | None = None
    ca_sign_file: str | None = None
    ca_sign_pass: str | None = None
    ca_verify_file: str | None = None
    ciphers: str | None = None
    ciphersuites: str | None = None
    client_sigalgs: str | None = None
    crl_file: str | None = None
    crt_ignore_err: str | None = None
    crt_list: str | None = None
    curves: str | None = None
    defer_accept: bool | None = None
    ecdhe: str | None = None
    expose_fd_listeners: bool | None = None
    force_sslv3: bool | None = None
    force_tlsv10: bool | None = None
    force_tlsv11: bool | None = None
    force_tlsv12: bool | None = None
    force_tlsv13: bool | None = None
    generate_certificates: bool | None = None
    gid: int | None = None
    group: str | None = None
    id: str | None = None
    interface: str | None = None
    level: RuntimeApiLevel | None = None
    maxconn: int | None = None
    mode: str | None = None
    mss: str | None = None
    name: str | None = Field(None, pattern=r'^\S+$')
    namespace: str | None = None
    nice: int | None = None
    no_alpn: bool | None = None
    no_ca_names: bool | None = None
    no_sslv3: bool | None = None
    no_tls_tickets: bool | None = None
    no_tlsv10: bool | None = None
    no_tlsv11: bool | None = None
    no_tlsv12: bool | None = None
    no_tlsv13: bool | None = None
    npn: str | None = None
    prefer_client_ciphers: bool | None = None
    process: str | None = Field(None, pattern=r'^\S+$')
    proto: str | None = None
    quic_cc_algo: QuicCcAlgo | None = None
    quic_force_retry: bool | None = None
    severity_output: SeverityOutput | None = None
    sigalgs: str | None = None
    ssl: bool | None = None
    ssl_cafile: str | None = Field(None, pattern=r'^\S+$')
    ssl_certificate: str | None = Field(None, pattern=r'^\S+$')
    ssl_max_ver: SslMaxVer | None = None
    ssl_min_ver: SslMinVer | None = None
    strict_sni: bool | None = None
    tcp_user_timeout: int | None = None
    tfo: bool | None = None
    thread: str | None = None
    tls_ticket_keys: str | None = None
    transparent: bool | None = None
    uid: str | None = None
    user: str | None = None
    v4v6: bool | None = None
    v6only: bool | None = None
    verify: str | None = None
    server_state_base: str | None = Field(None, pattern=r'^\S+$')
    server_state_file: str | None = Field(None, pattern=r'^\S+$')