"""Mail server information source."""

import json
from typing import Any, Dict, List

from langchain_noctis.sources.base import DomainInfoSource
from langchain_noctis.utils import RelationshipExtractor


class MailServerInfoSource(DomainInfoSource):
    """Mail server information source."""
    
    @property
    def info_type(self) -> str:
        return "mail_servers"
    
    def get_info(self, domain: str, **kwargs: Any) -> Dict[str, Any]:
        """Get mail server information for a specific domain."""
        response = self.domains_api.get_mail_servers(domain)
        # Convert Response object to dictionary if needed
        if hasattr(response, 'to_dict'):
            return response.to_dict()
        return response
    
    def format_info(self, domain: str, mail_info: Dict[str, Any]) -> str:
        """Format mail server information into readable text."""
        formatted_info = f"Mail Servers for {domain}:\n"
        
        if not isinstance(mail_info, dict):
            return f"{formatted_info}Raw response: {str(mail_info)}"
            
        if not mail_info or "relationships" not in mail_info:
            return f"{formatted_info}No mail server information available."
            
        if not mail_info["relationships"]:
            return f"{formatted_info}No mail server records found in the response."
        
        mx_records = self._extract_mail_server_records(mail_info)
        
        if mx_records:
            formatted_info += json.dumps(mx_records, indent=2)
        else:
            formatted_info += "No mail server records found in the response."
            
        return formatted_info
    
    def _extract_mail_server_records(
        self, mail_info: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract mail server records from the response.
        
        Args:
            mail_info: The mail server information from Noctis API.
            
        Returns:
            List of mail server records.
        """
        mx_records = []
        
        # Process relationships to extract mail server information
        for relation in mail_info.get("relationships", []):
            # Check for both MX_RECORD and hasMailHost relationship types
            if relation.get("middle") in ["MX_RECORD", "hasMailHost"]:
                left = relation.get("left", {})
                right = relation.get("right", {})
                
                # Extract domain and mail server info
                for domain_key, domain_value in left.items():
                    for mx_key, mx_value in right.items():
                        # Clean up mail server names
                        mail_server = RelationshipExtractor.clean_name(mx_key)
                            
                        mx_records.append({
                            "domain": domain_key,
                            "domain_info": domain_value,
                            "mail_server": mail_server,
                            "mail_server_info": mx_value,
                            "relationship_type": relation.get("middle")
                        })
                        
        return mx_records 