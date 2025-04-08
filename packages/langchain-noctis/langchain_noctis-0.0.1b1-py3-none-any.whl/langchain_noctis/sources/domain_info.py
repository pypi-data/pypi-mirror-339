"""Domain basic information source."""

import json
from typing import Any, Dict

from langchain_noctis.sources.base import DomainInfoSource


class DomainBasicInfoSource(DomainInfoSource):
    """Domain basic information source."""
    
    @property
    def info_type(self) -> str:
        return "domain_info"
    
    def get_info(self, domain: str, **kwargs: Any) -> Dict[str, Any]:
        """Get basic information for a specific domain."""
        response = self.domains_api.get_domain_info_card(domain)
        # Convert Response object to dictionary if needed
        if hasattr(response, 'to_dict'):
            return response.to_dict()
        return response
    
    def format_info(self, domain: str, domain_info: Dict[str, Any]) -> str:
        """Format domain information into readable text."""
        # Convert the domain information to a JSON string with indentation
        return f"Domain Information for {domain}:\n{json.dumps(domain_info, indent=2)}" 