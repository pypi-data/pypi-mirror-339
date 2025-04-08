"""Noctis tools."""

import json
import logging
import os
from typing import Any, Dict, List, Optional, Type

import noctis_sdk
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from noctis_sdk.rest import ApiException
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class NoctisToolInput(BaseModel):
    """Input schema for Noctis domain information tool.

    This docstring is **not** part of what is sent to the model when performing tool
    calling. The Field default values and descriptions **are** part of what is sent to
    the model when performing tool calling.
    """

    domain: str = Field(..., description="Domain name to retrieve information for")
    info_type: str = Field(
        "domain_info", 
        description=(
            "Type of information to retrieve. Options: domain_info, mail_servers, "
            "organization_domains, ip_sharing_domains, network_prefix_domains"
        )
    )


class NoctisTool(BaseTool):  # type: ignore[override]
    """Noctis domain information tool.

    This tool extracts information about a domain using the Noctis API. It can retrieve
    various types of information including basic domain details, mail servers, 
    organization domains, IP sharing domains, and network prefix domains.

    Setup:
        Install ``langchain-noctis`` and set environment variable ``NOCTIS_API_KEY``.

        .. code-block:: bash

            pip install -U langchain-noctis
            export NOCTIS_API_KEY="your-api-key"

    Instantiation:
        .. code-block:: python

            tool = NoctisTool()

    Invocation with args:
        .. code-block:: python

            tool.invoke({"domain": "example.com", "info_type": "domain_info"})

        .. code-block:: python

            # Returns domain information as a JSON string

    Invocation with ToolCall:

        .. code-block:: python

            tool.invoke({"args": {"domain": "example.com", "info_type": "domain_info"}, "id": "1", "name": tool.name, "type": "tool_call"})

        .. code-block:: python

            # Returns domain information as a JSON string
    """  # noqa: E501

    name: str = "noctis_domain_info"
    """The name that is passed to the model when performing tool calling."""
    description: str = (
        "Retrieves information about a domain using the Noctis API. "
        "Can get basic domain info, mail servers, and relationship data."
    )
    """The description that is passed to the model when performing tool calling."""
    args_schema: Type[BaseModel] = NoctisToolInput
    """The schema that is passed to the model when performing tool calling."""

    api_client: Any = None
    domains_api: Any = None
    def __init__(self, **kwargs: Any):
        """Initialize the NoctisTool."""
        super().__init__(**kwargs)
        
        # Set up API client with Authorization header
        if self.api_client is None:
            self.api_client = noctis_sdk.ApiClient(
                configuration=noctis_sdk.Configuration(
                    access_token=os.environ.get("NOCTIS_API_KEY")
                )
            )
        
        if self.domains_api is None:
            self.domains_api = noctis_sdk.DomainsApi(self.api_client)

    def _run(
        self, 
        domain: str, 
        info_type: str = "domain_info", 
        *, 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Run the tool to get domain information.
        
        Args:
            domain: The domain to get information for.
            info_type: The type of information to retrieve.
            run_manager: The callback manager for the tool run.
            
        Returns:
            Domain information as a formatted string.
        """
        try:
            if info_type == "domain_info":
                response = self.domains_api.get_domain_info_card(domain)
                return (
                    f"Domain Information for {domain}:\n"
                    f"{self._format_response(response)}"
                )
            
            elif info_type == "mail_servers":
                response = self.domains_api.get_mail_servers(domain)
                return f"Mail Servers for {domain}:\n{self._format_response(response)}"
            
            elif info_type == "organization_domains":
                response = self.domains_api.get_domains_by_same_organisation(domain)
                return self._format_relationship_response(
                    domain, 
                    response, 
                    "organization", 
                    "Domains managed by the same organization"
                )
            
            elif info_type == "ip_sharing_domains":
                response = self.domains_api.have_hosting_on_same_ip(domain)
                return self._format_relationship_response(
                    domain, 
                    response, 
                    "ip_sharing", 
                    "Domains sharing the same IP address"
                )
            
            elif info_type == "network_prefix_domains":
                response = self.domains_api.get_domains_on_same_network_prefix(domain)
                return self._format_relationship_response(
                    domain, 
                    response, 
                    "network_prefix", 
                    "Domains on the same network prefix"
                )
            
            else:
                return (
                    f"Unknown info_type: {info_type}. Available types are: "
                    f"domain_info, mail_servers, organization_domains, "
                    f"ip_sharing_domains, network_prefix_domains"
                )
                
        except ApiException as e:
            return f"Error retrieving {info_type} for {domain}: {str(e)}"
        except Exception as e:
            return f"Unexpected error retrieving {info_type} for {domain}: {str(e)}"
    
    def _format_response(self, response: Any) -> str:
        """Format API response to a string.
        
        Args:
            response: The API response to format.
            
        Returns:
            Formatted response as a string.
        """
        if hasattr(response, 'to_dict'):
            return json.dumps(response.to_dict(), indent=2)
        return str(response)
    
    def _format_relationship_response(
        self, 
        domain: str, 
        response: Any, 
        relationship_type: str, 
        entity_description: str
    ) -> str:
        """Format relationship response to a readable string.
        
        Args:
            domain: The domain queried.
            response: The API response to format.
            relationship_type: The type of relationship.
            entity_description: Description of the entity.
            
        Returns:
            Formatted relationship response as a string.
        """
        if hasattr(response, 'to_dict'):
            response_dict = response.to_dict()
        else:
            response_dict = response
            
        formatted_info = f"{entity_description} for {domain}:\n"
        
        if not isinstance(response_dict, dict) or not response_dict:
            return f"{formatted_info}No information available."
            
        if "relationships" not in response_dict or not response_dict["relationships"]:
            if relationship_type == "ip_sharing":
                return f"{formatted_info}No domains sharing the same IP found."
            elif relationship_type == "organization":
                return f"{formatted_info}No domains under the same organization found."
            elif relationship_type == "network_prefix":
                return f"{formatted_info}No domains on the same network prefix found."
            else:
                return f"{formatted_info}No related domains found."
        
        # Map relationship_type to actual API relationship names
        relationship_map = {
            "organization": "hasOrganisation",
            "ip_sharing": "hasIP",
            "network_prefix": "hasNetworkPrefix",
            "mail_servers": "hasMailHost"
        }
        
        # Get the actual relationship name to look for in the API response
        api_relationship_name = relationship_map.get(
            relationship_type, relationship_type
        )
        
        # Extract relationships of the specified type
        related_domains = self._extract_relationships(
            response_dict, api_relationship_name
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
            formatted_info += f"Found {len(unique_related_domains)} domains:\n"
            
            for item in unique_related_domains:
                formatted_info += f"- {item['related_entity']}\n"
        else:
            formatted_info += "No related domains found."
            
        return formatted_info
    
    def _extract_relationships(
        self, 
        data: Dict[str, Any], 
        relationship_type: str
    ) -> List[Dict[str, Any]]:
        """Extract relationships of a specific type from API response.
        
        Args:
            data: The API response data containing relationships
            relationship_type: The type of relationship to extract
            
        Returns:
            List of extracted relationships
        """
        results = []
        
        # Debug info about input data
        logger.debug(f"Extracting relationships of type '{relationship_type}'")
        logger.debug(f"Data structure: {json.dumps(data, indent=2)[:500]}...")
        
        if not isinstance(data, dict) or not data or "relationships" not in data:
            logger.debug("No relationships data found")
            return results
            
        if not data["relationships"]:
            logger.debug("Empty relationships array")
            return results
        
        # Log actual middle values in response for debugging
        middle_values = set()
        for relation in data.get("relationships", []):
            if "middle" in relation:
                middle_values.add(relation["middle"])
        logger.debug(f"Actual middle values in response: {middle_values}")
        
        for relation in data.get("relationships", []):
            if relation.get("middle") == relationship_type:
                left = relation.get("left", {})
                right = relation.get("right", {})
                
                # More detailed debug output
                logger.debug(f"Processing relationship: {relation.get('middle')}")
                logger.debug(f"Left: {left}")
                logger.debug(f"Right: {right}")
                
                for left_key, left_value in left.items():
                    for right_key, right_value in right.items():
                        # Clean up names if they have unwanted characters
                        right_clean = self._clean_name(right_key)
                        
                        results.append({
                            "primary_domain": left_key,
                            "related_entity": right_clean,
                            "primary_info": left_value,
                            "related_info": right_value,
                            "relationship_type": relation.get("middle")
                        })
        
        logger.debug(f"Found {len(results)} matching relationships")
        return results
    
    def _clean_name(self, name: str) -> str:
        """Clean up entity names by removing trailing braces and brackets.
        
        Args:
            name: The name to clean
            
        Returns:
            Cleaned name
        """
        # Remove trailing braces and brackets
        if "}" in name:
            name = name.split("}")[0]
        if "}}}]" in name:
            name = name.split("}}}]")[0]
        return name
