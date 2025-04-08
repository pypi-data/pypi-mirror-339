"""Registry for domain information sources."""

from typing import Dict, Optional

import noctis_sdk

from langchain_noctis.sources.base import DomainInfoSource
from langchain_noctis.sources.domain_info import DomainBasicInfoSource
from langchain_noctis.sources.ip_sharing_domains import IPSharingDomainsSource
from langchain_noctis.sources.mail_servers import MailServerInfoSource
from langchain_noctis.sources.network_prefix_domains import NetworkPrefixDomainsSource
from langchain_noctis.sources.organization_domains import OrganizationDomainsSource


class InfoSourceRegistry:
    """Registry for domain information sources."""
    
    def __init__(self, domains_api: noctis_sdk.DomainsApi):
        """Initialize the registry with available information sources.
        
        Args:
            domains_api: The Noctis domains API client.
        """
        self.domains_api = domains_api
        self._sources: Dict[str, DomainInfoSource] = {}
        
        # Register built-in sources
        self.register_source("domain_info", DomainBasicInfoSource(domains_api))
        self.register_source("mail_servers", MailServerInfoSource(domains_api))
        self.register_source(
            "organization_domains", 
            OrganizationDomainsSource(domains_api)
        )
        self.register_source(
            "ip_sharing_domains", 
            IPSharingDomainsSource(domains_api)
        )
        self.register_source(
            "network_prefix_domains", 
            NetworkPrefixDomainsSource(domains_api)
        )
    
    def register_source(self, name: str, source: DomainInfoSource) -> None:
        """Register a new information source.
        
        Args:
            name: The name to register the source under.
            source: The information source to register.
        """
        self._sources[name] = source
    
    def get_source(self, name: str) -> Optional[DomainInfoSource]:
        """Get an information source by name.
        
        Args:
            name: The name of the source to get.
            
        Returns:
            The information source, or None if not found.
        """
        return self._sources.get(name)
    
    def get_all_sources(self) -> Dict[str, DomainInfoSource]:
        """Get all registered information sources.
        
        Returns:
            Dictionary of all registered information sources.
        """
        return self._sources.copy() 