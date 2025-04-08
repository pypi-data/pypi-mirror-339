"""Base class for domain information sources."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import noctis_sdk
from langchain_core.documents import Document
from noctis_sdk.rest import ApiException

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
    def get_info(self, domain: str, **kwargs: Any) -> Dict[str, Any]:
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
    def format_info(self, domain: str, info: Dict[str, Any]) -> str:
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
    def call_api(self, domain: str, limit: int) -> Any:
        """Call the appropriate API method for this relationship type."""
        pass
    
    def get_info(self, domain: str, **kwargs: Any) -> Dict[str, Any]:
        """Get related domains based on the relationship type."""
        limit = kwargs.get("limit", self.limit)
        logger.debug(f"Calling API for {domain} with limit {limit}")
        try:
            response = self.call_api(domain, limit)
            if hasattr(response, 'to_dict'):
                dict_response = response.to_dict()
                logger.debug(
                    f"API response converted to dict with "
                    f"{len(dict_response.get('relationships', []))} relationships"
                )
                return dict_response
            return response
        except Exception as e:
            logger.error(f"Error in API call: {str(e)}")
            raise
    
    def format_info(self, domain: str, relationship_info: Dict[str, Any]) -> str:
        """Format relationship information into readable text."""
        formatted_info = f"{self.entity_description} {domain}:\n"
        
        if not isinstance(relationship_info, dict):
            return f"{formatted_info}Raw response: {str(relationship_info)}"
            
        # For empty response or no relationships, use specific error messages
        if not relationship_info:
            # Match exact expected string in tests
            if self.info_type == "ip_sharing_domains":
                return f"{formatted_info}No IP sharing domains information available."
            elif self.info_type == "organization_domains":
                return f"{formatted_info}No organization domains information available."
            else:
                return f"{formatted_info}No {self.info_type} information available."
            
        if "relationships" not in relationship_info:
            # Match exact expected string in tests
            if self.info_type == "ip_sharing_domains":
                return f"{formatted_info}No IP sharing domains information available."
            elif self.info_type == "organization_domains":
                return f"{formatted_info}No organization domains information available."
            else:
                return f"{formatted_info}No {self.info_type} information available."
        
        if not relationship_info["relationships"]:
            # Use specific empty messages for each source type to match tests
            if self.info_type == "ip_sharing_domains":
                return f"{formatted_info}No domains sharing the same IP found."
            elif self.info_type == "organization_domains":
                return f"{formatted_info}No domains under the same organization found."
            elif self.info_type == "network_prefix_domains":
                return f"{formatted_info}No domains on the same network prefix found."
            else:
                return f"{formatted_info}No {self.entity_description.lower()} found."
            
        # Extract relationships of the specified type
        related_domains = RelationshipExtractor.extract_relationships(
            relationship_info, self.relationship_type
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
            # Use specific formatting strings to match expected test output
            if self.info_type == "ip_sharing_domains":
                formatted_info += (
                    f"Found {len(unique_related_domains)} domains sharing "
                    f"the same IP address:\n"
                )
            elif self.info_type == "organization_domains":
                formatted_info += (
                    f"Found {len(unique_related_domains)} domains managed "
                    f"by the same organization:\n"
                )
            elif self.info_type == "network_prefix_domains":
                formatted_info += (
                    f"Found {len(unique_related_domains)} domains on the "
                    f"same network prefix:\n"
                )
            else:
                formatted_info += (
                    f"Found {len(unique_related_domains)} "
                    f"{self.entity_description.lower()}:\n"
                )
            
            for item in unique_related_domains:
                formatted_info += f"- {item['related_entity']}\n"
        else:
            formatted_info += f"No {self.entity_description.lower()} found."
            
        return formatted_info 