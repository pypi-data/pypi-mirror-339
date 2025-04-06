# haproxy-fusion-client

A Python client and service wrapper for interacting with the [HAProxy Fusion API](https://www.haproxy.com/products/fusion/).

## Features

- Authenticates with HAProxy Fusion
- Fetches configured frontend hosts
- Filter by cluster names

## Installation

```bash
pip install haproxy-fusion-client
```

## Usage

```python
from haproxy_fusion.api.haproxy_fusion_api_client import HAProxyFusionAPIClient
from haproxy_fusion.haproxy_fusion_service import HAProxyFusionService

haproxy_api_client = HAProxyFusionAPIClient(
    base_url="https://your-haproxy-fusion-url",
    username="your-username",
    password="your-password",
    verify=False
)

haproxy = HAProxyFusionService(haproxy_api_client)

include_clusters = ["Cluster1", "Cluster2"]
frontends = haproxy.get_configured_frontend_hosts(include_clusters)
print(frontends)
```

## Low-level API Access

You can use the `HAProxyFusionAPIClient` directly if you want more control:

```python
from haproxy_fusion.api.haproxy_fusion_api_client import HAProxyFusionAPIClient

client = HAProxyFusionAPIClient(
    base_url="https://your-haproxy-fusion-url",
    username="your-username",
    password="your-password",
    verify=False
)

response = client.get("/v1/clusters")
print(response.json())
```
