"""Base class for domain information sources."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

import noctis_sdk
from langchain_core.documents import Document
from noctis_sdk.models.response import Response
from noctis_sdk.rest import ApiException

from langchain_noctis.sources.enums import InfoType
from langchain_noctis.utils import RelationshipExtractor

# Set up logging
logger = logging.getLogger(__name__)

class DomainInfoSource(ABC):
    """Abstract base class for domain information sources."""
    
    def __init__(self, domains_api: noctis_sdk.DomainsApi):
        """Initialize the information source with the domains API client.
        
        Args:
            domains_api: The Noctis domains API client.
        """
        self.domains_api = domains_api
    
    @property
    @abstractmethod
    def info_type(self) -> str:
        """Return the type of information provided by this source."""
        pass
    
    @abstractmethod
    def get_info(self, domain: str, **kwargs: Any) -> Union[Dict[str, Any], Response]:
        """Get information for a specific domain.
        
        Args:
            domain: The domain name to query.
            
        Returns:
            Domain information from the Noctis API.
            
        Raises:
            ApiException: If there's an error in the API call.
        """
        pass
    
    @abstractmethod
    def format_info(self, domain: str, info: Union[Dict[str, Any], Response]) -> str:
        """Format domain information into readable text.
        
        Args:
            domain: The domain name.
            info: The domain information from Noctis API.
            
        Returns:
            Formatted string containing domain information.
        """
        pass
    
    def process(self, domain: str, **kwargs: Any) -> Optional[Document]:
        """Process a domain and create a document with its information.
        
        Args:
            domain: The domain name to process.
            
        Returns:
            A Document with the domain information, or None if there was an error.
        """
        try:
            logger.debug(f"Processing {self.info_type} for domain {domain}")
            api_response = self.get_info(domain, **kwargs)
            page_content = self.format_info(domain, api_response)
            
            return Document(
                page_content=page_content,
                metadata={
                    "domain": domain,
                    "source": "noctis_api",
                    "info_type": self.info_type,
                    "document_type": self.info_type,
                    "raw_response": api_response
                }
            )
        except ApiException as e:
            error_msg = (
                f"Exception when retrieving {self.info_type} "
                f"for {domain}: {str(e)}"
            )
            logger.warning(error_msg)
            return Document(
                page_content=error_msg,
                metadata={
                    "error": str(e), 
                    "domain": domain,
                    "info_type": self.info_type,
                    "document_type": self.info_type
                }
            )
        except Exception as e:
            error_msg = (
                f"Unexpected error when retrieving {self.info_type} "
                f"for {domain}: {str(e)}"
            )
            logger.exception(error_msg)
            return Document(
                page_content=error_msg,
                metadata={
                    "error": str(e), 
                    "domain": domain,
                    "info_type": self.info_type,
                    "document_type": self.info_type
                }
            ) 

class RelationshipInfoSource(DomainInfoSource):
    """Base class for sources that process relationship-based domain information."""
    
    def __init__(self, domains_api: noctis_sdk.DomainsApi, limit: int = 25):
        """Initialize with a limit on the number of relationships to return.
        
        Args:
            domains_api: The Noctis domains API client.
            limit: Maximum number of relationships to return.
        """
        super().__init__(domains_api)
        self.limit = limit
    
    @property
    @abstractmethod
    def relationship_type(self) -> str:
        """Return the type of relationship this source processes."""
        pass
    
    @property
    @abstractmethod
    def entity_description(self) -> str:
        """Return a description of the entities related to the domain."""
        pass
    
    @abstractmethod
    def call_api(self, domain: str, limit: int) -> Response:
        """Call the appropriate API method for this relationship type."""
        pass
    
    def get_info(self, domain: str, **kwargs: Any) -> Response:
        """Get related domains based on the relationship type."""
        limit = kwargs.get("limit", self.limit)
        logger.debug(f"Calling API for {domain} with limit {limit}")
        try:
            response = self.call_api(domain, limit)
            logger.debug(
                f"API response received with "
                f"{len(response.relationships) if response.relationships else 0} "
                f"relationships"
            )
            return response
        except Exception as e:
            logger.error(f"Error in API call: {str(e)}")
            raise
    
    def get_header_text(self, domain: str) -> str:
        """Get the header text for the formatted output.
        
        Args:
            domain: The domain being processed.
            
        Returns:
            Header text string.
        """
        is_name_server = (
            self.info_type == InfoType.MAIL_SERVERS or 
            self.info_type == InfoType.DOMAIN_NAME_SERVERS
        )
        if is_name_server:
            return f"{self.entity_description} for {domain}:\n"
        return f"{self.entity_description} as {domain}:\n"
    
    def get_empty_result_text(self) -> str:
        """Get text for when no relationships are found.
        
        Returns:
            Empty result text specific to this relationship type.
        """
        if self.info_type == InfoType.IP_SHARING_DOMAINS:
            return "No domains sharing the same IP found."
        elif self.info_type == InfoType.ORGANIZATION_DOMAINS:
            return "No domains under the same organization found."
        elif self.info_type == InfoType.NETWORK_PREFIX_DOMAINS:
            return "No domains on the same network prefix found."
        elif self.info_type == InfoType.DOMAIN_NAME_SERVERS:
            return "No name servers found."
        else:
            return f"No {self.entity_description.lower()} found."
            
    def get_found_items_header(self, count: int) -> str:
        """Get text for the header showing count of found items.
        
        Args:
            count: Number of items found.
            
        Returns:
            Header text for found items.
        """
        if self.info_type == InfoType.IP_SHARING_DOMAINS:
            return f"Found {count} domains sharing the same IP address:\n"
        elif self.info_type == InfoType.ORGANIZATION_DOMAINS:
            return f"Found {count} domains managed by the same organization:\n"
        elif self.info_type == InfoType.NETWORK_PREFIX_DOMAINS:
            return f"Found {count} domains on the same network prefix:\n"
        else:
            return f"Found {count} {self.entity_description.lower()}:\n"
    
    def format_info(self, domain: str, relationship_info: Response) -> str:
        """Format relationship information into readable text."""
        formatted_info = self.get_header_text(domain)
        
        if not relationship_info or not relationship_info.relationships:
            return formatted_info + self.get_empty_result_text()
            
        # Extract relationships of the specified type
        related_domains = RelationshipExtractor.extract_relationships(
            relationship_info, 
            self.relationship_type
        )
        
        # Deduplicate domains
        unique_domains = set()
        unique_related_domains = []
        
        for item in related_domains:
            related_domain = item["related_entity"]
            if related_domain not in unique_domains:
                unique_domains.add(related_domain)
                unique_related_domains.append(item)
        
        if unique_related_domains:
            formatted_info += self.get_found_items_header(len(unique_related_domains))
            
            for item in unique_related_domains:
                formatted_info += f"- {item['related_entity']}\n"
        else:
            formatted_info += self.get_empty_result_text()
            
        return formatted_info 