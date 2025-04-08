"""Mail server information source."""

import noctis_sdk
from noctis_sdk.models.response import Response

from langchain_noctis.sources.base import DomainInfoSource
from langchain_noctis.sources.enums import InfoType


class MailServerInfoSource(DomainInfoSource):
    """Mail server information source."""

    api_key_required = True

    @property
    def info_type(self) -> str:
        """Return the type of information provided by this source."""
        return InfoType.MAIL_SERVERS

    @property
    def relationship_type(self) -> str:
        """The relationship type."""
        return noctis_sdk.RelationshipType.HASMAIL.value

    @property
    def entity_description(self) -> str:
        """The entity description."""
        return "Mail Servers"

    def call_api(self, domain: str, limit: int = 10):
        """Call the API to get mail servers."""
        return self.domains_api.get_mail_servers(domain, limit=limit)

    def get_info(self, domain: str, limit: int = 10) -> Response:
        """
        Gets mail server information for a domain.

        Args:
            domain: The domain to look up.
            limit: Maximum number of results to return.

        Returns:
            Response object with mail server information.
        """
        try:
            mail_info = self.call_api(domain, limit=limit)
            return mail_info
        except Exception as e:
            return self.format_error(domain, e)

    def format_error(self, domain: str, error: Exception) -> Response:
        """Format an error as a Response object.
        
        Args:
            domain: The domain that was being looked up.
            error: The exception that was raised.
            
        Returns:
            A Response object with the error information.
        """
        return Response(error=str(error))

    def format_info(self, domain: str, mail_info: Response) -> str:
        """
        Format response as string.

        Args:
            domain: The domain we looked up information for.
            mail_info: The mail server information.

        Returns:
            The formatted information.
        """
        # Check for error in the response
        if hasattr(mail_info, "error") and mail_info.error:
            return f"Error getting mail server info for {domain}: {mail_info.error}"

        formatted_info = f"{self.entity_description} for {domain}:\n"
        mx_records = []

        # Extract MX records from the response
        if mail_info.relationships:
            for relation in mail_info.relationships:
                # Check for both MX_RECORD and hasMailHost relationship types
                relation_types = [
                    "MX_RECORD", 
                    noctis_sdk.RelationshipType.HASMAILHOST.value
                ]
                if hasattr(relation, 'middle') and relation.middle in relation_types:
                    right = relation.right if hasattr(relation, 'right') else {}
                    
                    # Extract MX record information
                    if isinstance(right, dict):
                        # Format 1: dictionary with 'value' key
                        # Format 2: dictionary with host names as keys
                        if 'value' in right:
                            host = right.get('value', '')
                            priority = right.get('priority', '')
                            if host:
                                mx_records.append({"host": host, "priority": priority})
                        else:
                            # Handle dictionary with MX host names as keys
                            for host, host_type in right.items():
                                if host_type == "MX_HOST" or "mx" in host.lower():
                                    mx_records.append({"host": host, "priority": ""})

        # Format the MX records information
        if mx_records:
            # Sort by priority if available
            mx_records = sorted(
                mx_records, 
                key=lambda x: int(x["priority"]) if x["priority"] else 999
            )

            formatted_info += "Found the following mail servers:\n"
            for record in mx_records:
                if record["priority"]:
                    formatted_info += (
                        f"- {record['host']} (priority: {record['priority']})\n"
                    )
                else:
                    formatted_info += f"- {record['host']}\n"
        else:
            formatted_info += "No mail server records found.\n"

        return formatted_info 