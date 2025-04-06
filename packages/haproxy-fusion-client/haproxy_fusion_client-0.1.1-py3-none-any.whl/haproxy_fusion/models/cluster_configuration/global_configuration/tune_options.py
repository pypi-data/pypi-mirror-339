from pydantic import Field

from haproxy_fusion.models.base.base_model import BaseModel


class TuneOptions(BaseModel):
    buffers_limit: int | None = None
    buffers_reserve: int | None = Field(None, ge=2)
    bufsize: int | None = None
    comp_maxlevel: int | None = None
    fail_alloc: bool | None = None
    fd_edge_triggered: str | None = Field(None, pattern="^(enabled|disabled)$")

    h2_be_initial_window_size: int | None = None
    h2_be_max_concurrent_streams: int | None = None
    h2_fe_initial_window_size: int | None = None
    h2_fe_max_concurrent_streams: int | None = None
    h2_header_table_size: int | None = Field(None, le=65535)
    h2_initial_window_size: int | None = None
    h2_max_concurrent_streams: int | None = None
    h2_max_frame_size: int | None = None

    http_cookielen: int | None = None
    http_logurilen: int | None = None
    http_maxhdr: int | None = Field(None, ge=1, le=32767)

    idle_pool_shared: str | None = Field(None, pattern="^(enabled|disabled)$")
    idletimer: int | None = Field(None, ge=0, le=65535)

    listener_default_shards: str | None = Field(None, pattern="^(by-process|by-thread|by-group)$")
    listener_multi_queue: str | None = Field(None, pattern="^(enabled|disabled)$")

    lua_burst_timeout: int | None = None
    lua_forced_yield: int | None = None
    lua_maxmem: bool | None = None
    lua_service_timeout: int | None = None
    lua_session_timeout: int | None = None
    lua_task_timeout: int | None = None

    maxaccept: int | None = None
    maxpollevents: int | None = None
    maxrewrite: int | None = None
    memory_hot_size: int | None = None
    pattern_cache_size: int | None = None
    peers_max_updates_at_once: int | None = None
    pipesize: int | None = None
    pool_high_fd_ratio: int | None = None
    pool_low_fd_ratio: int | None = None

    quic_frontend_conn_tx_buffers_limit: int | None = None
    quic_frontend_max_idle_timeout: int | None = None
    quic_frontend_max_streams_bidi: int | None = None
    quic_max_frame_loss: int | None = None
    quic_retry_threshold: int | None = None
    quic_socket_owner: str | None = Field(None, pattern="^(listener|connection)$")

    rcvbuf_client: int | None = None
    rcvbuf_server: int | None = None
    recv_enough: int | None = None
    runqueue_depth: int | None = None
    sched_low_latency: str | None = Field(None, pattern="^(enabled|disabled)$")
    sndbuf_client: int | None = None
    sndbuf_server: int | None = None

    ssl_cachesize: int | None = None
    ssl_capture_buffer_size: int | None = None
    ssl_ctx_cache_size: int | None = None
    ssl_default_dh_param: int | None = None
    ssl_force_private_cache: bool | None = None
    ssl_keylog: str | None = Field(None, pattern="^(enabled|disabled)$")
    ssl_lifetime: int | None = None
    ssl_maxrecord: int | None = None
    ssl_ocsp_update_max_delay: int | None = None
    ssl_ocsp_update_min_delay: int | None = None

    stick_counters: int | None = None
    vars_global_max_size: int | None = None
    vars_proc_max_size: int | None = None
    vars_reqres_max_size: int | None = None
    vars_sess_max_size: int | None = None
    vars_txn_max_size: int | None = None

    zlib_memlevel: int | None = Field(None, ge=1, le=9)
    zlib_windowsize: int | None = Field(None, ge=8, le=15)
