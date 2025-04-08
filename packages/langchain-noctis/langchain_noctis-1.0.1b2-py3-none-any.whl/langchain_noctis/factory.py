"""Factory for creating information sources."""

from typing import Any, Dict, Optional, Type

import noctis_sdk

from langchain_noctis.config import NoctisConfig
from langchain_noctis.sources.base import DomainInfoSource
from langchain_noctis.sources.domain_info import DomainBasicInfoSource
from langchain_noctis.sources.domain_name_servers import DomainNameServersSource
from langchain_noctis.sources.enums import InfoType
from langchain_noctis.sources.ip_sharing_domains import IPSharingDomainsSource
from langchain_noctis.sources.mail_servers import MailServerInfoSource
from langchain_noctis.sources.network_prefix_domains import NetworkPrefixDomainsSource
from langchain_noctis.sources.organization_domains import OrganizationDomainsSource


class InfoSourceFactory:
    """Factory for creating Noctis information sources.
    
    This class is responsible for creating instances of different information
    sources for the Noctis API.
    """
    
    _source_classes: Dict[str, Type[DomainInfoSource]] = {
        InfoType.DOMAIN_INFO: DomainBasicInfoSource,
        InfoType.MAIL_SERVERS: MailServerInfoSource,
        InfoType.ORGANIZATION_DOMAINS: OrganizationDomainsSource,
        InfoType.IP_SHARING_DOMAINS: IPSharingDomainsSource,
        InfoType.NETWORK_PREFIX_DOMAINS: NetworkPrefixDomainsSource,
        InfoType.DOMAIN_NAME_SERVERS: DomainNameServersSource,
    }
    
    @classmethod
    def create_source(
        cls, 
        source_type: str, 
        domains_api: Optional[noctis_sdk.DomainsApi] = None, 
        **kwargs: Any
    ) -> DomainInfoSource:
        """Create an information source of the given type.
        
        Args:
            source_type: The type of information source to create
            domains_api: The domains API client to use (optional, uses config if None)
            **kwargs: Additional keyword arguments to pass to the source constructor
        
        Returns:
            An initialized DomainInfoSource instance
            
        Raises:
            ValueError: If the source type is invalid
        """
        if source_type not in cls._source_classes:
            raise ValueError(
                f"Unsupported source type: {source_type}. "
                f"Supported types: {', '.join(cls._source_classes.keys())}"
            )
        
        # Use provided domains_api or get from config
        if domains_api is None:
            config = NoctisConfig()
            domains_api = config.domains_api
            
        # Create the source instance
        source_class = cls._source_classes[source_type]
        return source_class(domains_api, **kwargs)
    
    @classmethod
    def register_source_class(
        cls, source_type: str, source_class: Type[DomainInfoSource]
    ) -> None:
        """Register a new source class.
        
        Args:
            source_type: The name to register the source class under
            source_class: The source class to register
        """
        cls._source_classes[source_type] = source_class
        
    @classmethod
    def create_all_sources(
        cls, domains_api: noctis_sdk.DomainsApi = None
    ) -> Dict[str, DomainInfoSource]:
        """Create instances of all registered source types.
        
        Args:
            domains_api: The domains API client to use (optional)
            
        Returns:
            Dictionary mapping source type names to source instances
        """
        return {
            source_type: cls.create_source(source_type, domains_api)
            for source_type in cls._source_classes
        } 