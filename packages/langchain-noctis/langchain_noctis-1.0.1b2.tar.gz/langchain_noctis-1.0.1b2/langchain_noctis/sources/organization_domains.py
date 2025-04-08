"""Organization domains information source."""

import noctis_sdk
from noctis_sdk.models.response import Response

from langchain_noctis.sources.base import RelationshipInfoSource
from langchain_noctis.sources.enums import InfoType


class OrganizationDomainsSource(RelationshipInfoSource):
    """Organization domains information source."""
    
    @property
    def info_type(self) -> str:
        """Return the type of information provided by this source."""
        return InfoType.ORGANIZATION_DOMAINS
    
    @property
    def relationship_type(self) -> str:
        return noctis_sdk.RelationshipType.HASORGANISATION.value
    
    @property
    def entity_description(self) -> str:
        return "Domains managed by the same organization"
    
    def call_api(self, domain: str, limit: int) -> Response:
        """Call the API to get domains managed by the same organization."""
        return self.domains_api.get_domains_by_same_organisation(domain, limit=limit) 