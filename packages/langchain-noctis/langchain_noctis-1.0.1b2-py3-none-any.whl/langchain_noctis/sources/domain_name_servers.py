"""Domain name servers information source."""

import noctis_sdk
from noctis_sdk.models.response import Response

from langchain_noctis.sources.base import RelationshipInfoSource
from langchain_noctis.sources.enums import InfoType


class DomainNameServersSource(RelationshipInfoSource):
    """Domain name servers information source."""
    
    @property
    def info_type(self) -> str:
        """Return the type of information provided by this source."""
        return InfoType.DOMAIN_NAME_SERVERS
    
    @property
    def relationship_type(self) -> str:
        return noctis_sdk.RelationshipType.HASNAMESERVER.value
    
    @property
    def entity_description(self) -> str:
        return "Name servers"
    
    def call_api(self, domain: str, limit: int) -> Response:
        """Call the API to get domain name servers."""
        return self.domains_api.get_name_servers(domain, limit=limit) 