"""Source registry for information sources."""

import logging
from typing import Dict, List, Optional, Union

import noctis_sdk

from langchain_noctis.factory import InfoSourceFactory
from langchain_noctis.sources.base import DomainInfoSource
from langchain_noctis.sources.enums import InfoType

# Set up logging
logger = logging.getLogger(__name__)


class InfoSourceRegistry:
    """Registry for domain information sources.
    
    The registry manages the creation and caching of information sources,
    and keeps track of which sources are enabled. It uses the InfoSourceFactory
    to create new sources when requested.
    """
    
    def __init__(
        self, 
        domains_api: Optional[noctis_sdk.DomainsApi] = None,
        default_sources: Optional[List[str]] = None
    ):
        """Initialize the registry with the given domains API client.
        
        Args:
            domains_api: The Noctis domains API client. If None, uses config.
            default_sources: Source types to enable by default. If None, uses
                DOMAIN_INFO only.
        """
        # Use provided domains_api or get from config
        from langchain_noctis.config import NoctisConfig
        self.domains_api = domains_api or NoctisConfig().domains_api
        
        # Set up source cache and factory
        self._sources: Dict[str, DomainInfoSource] = {}
        self._factory = InfoSourceFactory()
        
        # Start with default enabled sources
        if default_sources is None:
            default_sources = [InfoType.DOMAIN_INFO]
            
        self.enabled_sources = default_sources.copy()
        
        # Register all default sources
        self._register_default_sources()
    
    def _register_default_sources(self) -> None:
        """Register all built-in information sources."""
        # Use the factory to create all sources
        sources = InfoSourceFactory.create_all_sources(self.domains_api)
        for source_type, source in sources.items():
            self.register_source(source_type, source)
    
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
        # Try to get an existing source first
        source = self._sources.get(name)
        
        # If not found but it's a known type, create it on demand
        if source is None:
            try:
                source = InfoSourceFactory.create_source(name, self.domains_api)
                self.register_source(name, source)
            except ValueError:
                # Not a known source type
                return None
                
        return source
    
    def get_all_sources(self) -> Dict[str, DomainInfoSource]:
        """Get all registered information sources.
        
        Returns:
            Dictionary of all registered information sources.
        """
        return self._sources.copy()
        
    def add_info_source(
        self, 
        name: str, 
        source: Union[DomainInfoSource, type], 
        enable: bool = True
    ) -> None:
        """
        Add a new information source to the registry.
        
        Args:
            name: The name to register the source under.
            source: The information source to add or a source class.
            enable: Whether to enable the source by default.
        """
        # If source is a class, register it with the factory
        if isinstance(source, type) and issubclass(source, DomainInfoSource):
            InfoSourceFactory.register_source_class(name, source)
            source = InfoSourceFactory.create_source(name, self.domains_api)
            
        self.register_source(name, source)
        if enable and name not in self.enabled_sources:
            self.enabled_sources.append(name)

    def enable_source(self, name: str) -> bool:
        """
        Enable an information source.
        
        Args:
            name: The name of the source to enable.
            
        Returns:
            True if the source was found and enabled, False otherwise.
        """
        source = self.get_source(name)
        if source is not None:
            if name not in self.enabled_sources:
                self.enabled_sources.append(name)
            return True
        return False
        
    def disable_source(self, name: str) -> None:
        """
        Disable an information source.
        
        Args:
            name: The name of the source to disable.
        """
        if name in self.enabled_sources:
            self.enabled_sources.remove(name) 