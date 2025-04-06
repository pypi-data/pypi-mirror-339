from haproxy_fusion.api.haproxy_fusion_api_client import HAProxyFusionAPIClient

import re

import dns.resolver
from typing import Callable

from haproxy_fusion.models.cluster.cluster import Cluster
from haproxy_fusion.models.frontend.enum.frontend_mode import FrontendMode
from haproxy_fusion.models.frontend.frontend import Frontend


class HAProxyFusionService:
    """
    High-level interface for interacting with HAProxy Fusion clusters and frontends,
    built on top of the HAProxyFusionAPIClient.
    """

    def __init__(self, haproxy_fusion_api_client: HAProxyFusionAPIClient, dns_server_ip: str = "8.8.8.8"):
        self.haproxy_fusion_api_client = haproxy_fusion_api_client
        self.dns_server_ip = dns_server_ip

    def get_clusters(
            self,
            filter_func: Callable[[Cluster], bool] | None = None,
            include_name_list: list[str] | None = None,
            exclude_name_list: list[str] | None = None,
            exclude_name_keyword: str | None = None
    ) -> list[Cluster]:
        """
        Fetches clusters from the API and applies optional filters:
        - include_name_list: only return clusters in this list
        - exclude_name_list: omit clusters in this list
        - filter_func: custom filtering logic
        - exclude_name_keyword: case-insensitive keyword filter
        """
        clusters = self.haproxy_fusion_api_client.get_clusters()

        if include_name_list is not None:
            clusters = [c for c in clusters if c.name in include_name_list]

        if exclude_name_list:
            clusters = [c for c in clusters if c.name not in exclude_name_list]

        if filter_func:
            clusters = [c for c in clusters if filter_func(c)]

        if exclude_name_keyword:
            clusters = [c for c in clusters if exclude_name_keyword.casefold() not in c.name.casefold()]

        return clusters

    def get_cluster_configuration(self, cluster_id: str):
        """
        Returns the full configuration for the given cluster.
        """
        return self.haproxy_fusion_api_client.get_cluster_configuration(cluster_id=cluster_id)

    def get_configured_frontend_hosts(self, include_clusters: list[str] = None) -> set[Frontend]:
        """
        Retrieves a set of unique frontend hostnames from ACLs that use 'hdr(host)'.

        - Only includes frontends for clusters listed in include_clusters.
        - Each returned Frontend contains its name, mode, and resolved FQDNs.
        """
        frontends_specified = set()

        clusters = self.get_clusters(include_name_list=include_clusters)
        for cluster in clusters:
            for frontend in self._get_frontends(cluster):
                for acl in frontend.get('acls', []):
                    if acl.get('criterion') == "hdr(host)":
                        fqdns = self._extract_fqdns_from_acl(acl['value'])
                        frontends_specified.add(
                            Frontend(
                                name=frontend['name'],
                                mode=self._find_mode(frontend, fqdns),
                                fqdns=fqdns
                            )
                        )

        return frontends_specified

    def _get_frontends(self, cluster: Cluster) -> list[dict]:
        """
        Returns frontend definitions from a cluster configuration.
        """
        cluster_config = self.get_cluster_configuration(cluster.id)
        if cluster_config and cluster_config.frontends is not None:
            return cluster_config.frontends
        return []

    def _find_mode(self, frontend: dict, urls: list[str]) -> FrontendMode:
        """
        Determines the operational mode of a frontend based on DNS resolution and WAF configuration rules.

        - Returns ONBOARDING if none of the resolved FQDN IPs match the frontend's bound IPs.
        - Returns BLOCKING or LEARNING based on WAF rules and filters.
        - Defaults to CREATED if no specific conditions match.
        """
        resolved_ips = self._resolve_dns_ips(urls)
        bound_ips = {bind.get('address') for bind in frontend.get('binds', [])}

        if not resolved_ips & bound_ips:
            return FrontendMode.ONBOARDING

        waf_mode = self._determine_mode_from_waf_rules(frontend)
        return waf_mode if waf_mode else FrontendMode.CREATED

    def _resolve_dns_ips(self, urls: list[str]) -> set[str]:
        """
        Resolves A records for the given list of FQDNs using the configured DNS server.
        Returns a set of resolved IP addresses as strings.
        """
        resolved_ips = set()
        for url in urls:
            query = dns.message.make_query(url, dns.rdatatype.A)
            try:
                response = dns.query.tcp(query, self.dns_server_ip)
                for answer in response.answer:
                    if answer.rdtype == dns.rdatatype.A:
                        for rdata in answer.items:
                            resolved_ips.add(rdata.to_text())
            except Exception as e:
                print(f"DNS query failed for {url}: {e}")
        return resolved_ips

    @staticmethod
    def _determine_mode_from_waf_rules(frontend: dict) -> FrontendMode | None:
        """
        Inspects frontend configuration to detect WAF-related rules or filters.

        Returns:
        - BLOCKING if 'deny' rules mention 'waf' in condition tests
        - LEARNING if a 'waf' filter is present
        - None if no WAF indicators are found
        """
        if any(
                rule.get("type") == "deny" and "waf" in rule.get("cond_test", "")
                for rule in frontend.get("http_request_rules", [])
        ):
            return FrontendMode.BLOCKING

        if any(
                rule.get("type") == "deny" and "waf" in rule.get("cond_test", "")
                for rule in frontend.get("waf_body_rules", [])
        ):
            return FrontendMode.BLOCKING

        if any(filter_.get("type") == "waf" for filter_ in frontend.get("filters", [])):
            return FrontendMode.LEARNING

        return None

    @staticmethod
    def _extract_fqdns_from_acl(acl_value: str) -> list[str]:
        """
        Extracts a list of FQDNs from an ACL 'value' string, removing known modifiers and splitting on ORs.
        """
        cleaned_value = re.sub(r'\s*(-i|-m \w+)\s*', '', acl_value).strip()
        values = map(str.strip, re.split(r'\s*\|\|\s*|\s*OR\s*', cleaned_value))

        return list(values)
