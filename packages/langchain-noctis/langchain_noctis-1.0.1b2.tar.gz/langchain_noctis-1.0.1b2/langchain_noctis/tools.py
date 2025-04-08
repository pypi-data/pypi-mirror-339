"""Noctis tools."""

import logging
from typing import Any, Optional, Type

import noctis_sdk
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from noctis_sdk.rest import ApiException
from pydantic import BaseModel, Field

from langchain_noctis.config import NoctisConfig
from langchain_noctis.registry import InfoSourceRegistry
from langchain_noctis.sources.enums import InfoType

logger = logging.getLogger(__name__)


class NoctisToolInput(BaseModel):
    """Input schema for Noctis domain information tool.

    This docstring is **not** part of what is sent to the model when performing tool
    calling. The Field default values and descriptions **are** part of what is sent to
    the model when performing tool calling.
    """

    domain: str = Field(..., description="Domain name to retrieve information for")
    info_type: str = Field(
        InfoType.DOMAIN_INFO, 
        description=(
            f"Type of information to retrieve. Options: {InfoType.DOMAIN_INFO}, "
            f"{InfoType.MAIL_SERVERS}, {InfoType.ORGANIZATION_DOMAINS}, "
            f"{InfoType.IP_SHARING_DOMAINS}, {InfoType.NETWORK_PREFIX_DOMAINS}, "
            f"{InfoType.DOMAIN_NAME_SERVERS}"
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
        "Can get basic domain info, domain's mail servers, domain's name servers, "
        "domains managed by the same organization, domains sharing the same IP "
        "address, and domains on the same network prefix."
    )
    """The description that is passed to the model when performing tool calling."""
    args_schema: Type[BaseModel] = NoctisToolInput
    """The schema that is passed to the model when performing tool calling."""

    source_registry: Optional[InfoSourceRegistry] = None

    def __init__(
        self,
        api_client: Optional[noctis_sdk.ApiClient] = None,
        domains_api: Optional[noctis_sdk.DomainsApi] = None,
        asns_api: Optional[noctis_sdk.AsnsApi] = None,
        source_registry: Optional[InfoSourceRegistry] = None,
        **kwargs: Any
    ):
        """Initialize the NoctisTool.
        
        Args:
            api_client: Optional API client to use
            domains_api: Optional domains API client to use
            asns_api: Optional ASNs API client to use
            source_registry: Optional source registry to use
            **kwargs: Additional keyword arguments
        """
        super().__init__(**kwargs)
        
        # Get the configuration
        self._config = NoctisConfig()
        
        # Set up source registry - use domains_api from config if not provided
        domains_api = domains_api or self._config.domains_api
        self.source_registry = source_registry or InfoSourceRegistry(domains_api)
            
    def _run(
        self, 
        domain: str, 
        info_type: str = InfoType.DOMAIN_INFO, 
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
            # Get the appropriate source from the registry
            source = self.source_registry.get_source(info_type)
            
            if source is not None:
                # Use the source to process the domain
                document = source.process(domain)
                if document:
                    return document.page_content
                return f"No information available for {domain} using {info_type}."
            else:
                return (
                    f"Unknown info_type: {info_type}. Available types are: "
                    f"{', '.join(self.source_registry.enabled_sources)}"
                )
                
        except ApiException as e:
            return f"Error retrieving {info_type} for {domain}: {str(e)}"
        except Exception as e:
            return f"Unexpected error retrieving {info_type} for {domain}: {str(e)}"
