"""IP sharing domains information source."""

from typing import Any

from langchain_noctis.sources.base import RelationshipInfoSource


class IPSharingDomainsSource(RelationshipInfoSource):
    """IP sharing domains information source."""
    
    @property
    def info_type(self) -> str:
        return "ip_sharing_domains"
    
    @property
    def relationship_type(self) -> str:
        return "hasIP"
    
    @property
    def entity_description(self) -> str:
        return "Domains sharing the same IP address as"
    
    def call_api(self, domain: str, limit: int) -> Any:
        """Call the API to get domains sharing the same IP address."""
        return self.domains_api.have_hosting_on_same_ip(domain, limit=limit) 