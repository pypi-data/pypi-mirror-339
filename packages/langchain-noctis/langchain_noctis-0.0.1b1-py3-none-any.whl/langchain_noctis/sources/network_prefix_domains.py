"""Network prefix domains information source."""

from typing import Any

from langchain_noctis.sources.base import RelationshipInfoSource


class NetworkPrefixDomainsSource(RelationshipInfoSource):
    """Source for domains on the same network prefix."""
    
    @property
    def info_type(self) -> str:
        return "network_prefix_domains"
    
    @property
    def relationship_type(self) -> str:
        return "hasIP"
    
    @property
    def entity_description(self) -> str:
        return "Domains on the same network prefix as"
    
    def call_api(self, domain: str, limit: int) -> Any:
        """Call the API to get domains on the same network prefix."""
        return self.domains_api.get_domains_on_same_network_prefix(domain, limit=limit) 