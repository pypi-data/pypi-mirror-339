"""Organization domains information source."""

from typing import Any

from langchain_noctis.sources.base import RelationshipInfoSource


class OrganizationDomainsSource(RelationshipInfoSource):
    """Organization domains information source."""
    
    @property
    def info_type(self) -> str:
        return "organization_domains"
    
    @property
    def relationship_type(self) -> str:
        return "hasOrganisation"
    
    @property
    def entity_description(self) -> str:
        return "Domains managed by the same organization as"
    
    def call_api(self, domain: str, limit: int) -> Any:
        """Call the API to get domains managed by the same organization."""
        return self.domains_api.get_domains_by_same_organisation(domain, limit=limit) 