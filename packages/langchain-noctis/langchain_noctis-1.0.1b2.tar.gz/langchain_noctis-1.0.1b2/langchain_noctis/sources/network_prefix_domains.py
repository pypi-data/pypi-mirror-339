"""Network prefix domains information source."""

import noctis_sdk
from noctis_sdk.models.response import Response

from langchain_noctis.sources.base import RelationshipInfoSource
from langchain_noctis.sources.enums import InfoType


class NetworkPrefixDomainsSource(RelationshipInfoSource):
    """Source for domains on the same network prefix."""
    
    @property
    def info_type(self) -> str:
        """Return the type of information provided by this source."""
        return InfoType.NETWORK_PREFIX_DOMAINS
    
    @property
    def relationship_type(self) -> str:
        return noctis_sdk.RelationshipType.HASIP.value
    
    @property
    def entity_description(self) -> str:
        return "Domains on the same network prefix"
    
    def call_api(self, domain: str, limit: int) -> Response:
        """Call the API to get domains on the same network prefix."""
        return self.domains_api.get_domains_on_same_network_prefix(domain, limit=limit) 