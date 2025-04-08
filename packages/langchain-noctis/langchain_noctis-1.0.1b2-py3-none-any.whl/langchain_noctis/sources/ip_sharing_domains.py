"""IP sharing domains information source."""

import noctis_sdk
from noctis_sdk.models.response import Response

from langchain_noctis.sources.base import RelationshipInfoSource
from langchain_noctis.sources.enums import InfoType


class IPSharingDomainsSource(RelationshipInfoSource):
    """IP sharing domains information source."""
    
    @property
    def info_type(self) -> str:
        """Return the type of information provided by this source."""
        return InfoType.IP_SHARING_DOMAINS
    
    @property
    def relationship_type(self) -> str:
        return noctis_sdk.RelationshipType.HASIP.value
    
    @property
    def entity_description(self) -> str:
        return "Domains sharing the same IP address"
    
    def call_api(self, domain: str, limit: int) -> Response:
        """Call the API to get domains sharing the same IP."""
        return self.domains_api.have_hosting_on_same_ip(domain, limit=limit) 