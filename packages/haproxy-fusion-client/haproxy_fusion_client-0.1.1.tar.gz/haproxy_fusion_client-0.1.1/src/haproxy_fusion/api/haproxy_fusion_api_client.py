import requests
from requests.auth import HTTPBasicAuth

from haproxy_fusion.models.cluster.cluster import Cluster
from haproxy_fusion.models.cluster_configuration.cluster_configuration import ClusterConfiguration


class HAProxyFusionAPIClient:
    def __init__(self, base_url: str, username: str = None, password: str = None, api_key: str = None,
                 verify: bool = True):
        """
        Initializes the API client.
        Supports either Basic Authentication (username & password) or API Key Authentication.

        :param base_url: Base URL of the HAProxy Fusion API.
        :param username: Username for Basic Authentication (optional if using API key).
        :param password: Password for Basic Authentication (optional if using API key).
        :param api_key: API key for authentication (optional if using Basic Auth).
        """
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.api_key = api_key
        self.verify = verify

        if (self.username and self.password) and self.api_key:
            raise ValueError("Provide either API Key or Basic Authentication, not both.")

        if not (self.api_key or (self.username and self.password)):
            raise ValueError("You must provide either API Key or Basic Authentication.")

    @property
    def _api_url(self) -> str:
        return f"{self.base_url}/v1"

    def _get_headers(self) -> dict[str, str]:
        """
        Generates headers for requests based on authentication method.
        """
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _get_auth(self) -> HTTPBasicAuth:
        """
        Returns authentication object for Basic Auth if applicable.
        """
        return HTTPBasicAuth(self.username, self.password) if self.username and self.password else None

    def request(self, method: str, endpoint: str, params: dict[str, any] = None,
                data: dict[str, any] = None) -> requests.Response:
        """
        Generic request method that handles authentication.

        :param method: HTTP method (GET, POST, etc.).
        :param endpoint: API endpoint (without base URL).
        :param params: Query parameters (optional).
        :param data: JSON payload (optional).
        :return: Response object from the request.
        """
        url = f"{self._api_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers()
        auth = self._get_auth()

        response = requests.request(
            method=method.upper(),
            url=url,
            headers=headers,
            auth=auth,
            verify=self.verify,
            params=params,
            json=data
        )

        response.raise_for_status()
        return response

    def get(self, endpoint: str, params: dict[str, any] = None) -> any:
        """
        Performs a GET request and returns the parsed JSON response.

        :param endpoint: API endpoint to fetch.
        :param params: Optional query parameters.
        :return: Parsed JSON response (could be dict or list depending on the API response).
        """
        return self.request("GET", endpoint, params=params).json()

    def post(self, endpoint: str, data: dict[str, any]) -> any:
        """
        Performs a POST request and returns the parsed JSON response.

        :param endpoint: API endpoint to post to.
        :param data: JSON payload to send.
        :return: Parsed JSON response (could be dict or list depending on the API response).
        """
        return self.request("POST", endpoint, data=data).json()

    def get_clusters(self) -> list[Cluster]:
        """
        Fetches and returns a list of Cluster objects from the HAProxy Fusion API.

        :return: List of Cluster instances.
        """
        return [Cluster.model_validate(item) for item in self.get("/clusters")]

    def get_cluster_by_id(self, cluster_id: str) -> dict[str, any]:
        """
        Fetches and returns details of a specific cluster by its ID.

        :param cluster_id: The unique ID of the cluster.
        :return: Dictionary containing the cluster details.
        """
        return self.get(f"/clusters/{cluster_id}")

    def get_cluster_configuration(self, cluster_id: str) -> ClusterConfiguration:
        """
        Fetches and returns a ClusterConfiguration object by the cluster's ID.

        :param cluster_id: The unique ID of the cluster.
        :return: ClusterConfiguration instance containing the cluster configuration details.
        """
        return ClusterConfiguration.model_validate(
            self.get(f"/clusters/{cluster_id}/services/haproxy/configuration/structured")
        )
