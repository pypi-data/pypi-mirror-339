"""Configuration module for Noctis integration.

Provides centralized configuration and API client management for Noctis integration.
"""

import os
from typing import Optional

import noctis_sdk


class NoctisConfig:
    """Configuration for Noctis API integration.
    
    This class serves as a central configuration point for Noctis API credentials
    and client instances, following the Dependency Inversion Principle.
    """
    
    _instance = None  # Singleton instance
    
    def __new__(cls, api_key: Optional[str] = None):
        """Create or return the singleton instance."""
        if cls._instance is None:
            cls._instance = super(NoctisConfig, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Noctis configuration.
        
        Args:
            api_key: Optional API key. If None, will try to get from environment.
        """
        # Skip re-initialization of singleton
        if getattr(self, '_initialized', False):
            return
            
        self.api_key = api_key or os.environ.get("NOCTIS_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided either as an argument or via "
                "NOCTIS_API_KEY environment variable"
            )
        
        # Initialize the configurations and clients
        self._api_client = None
        self._domains_api = None
        self._asns_api = None
        self._initialized = True
    
    @property
    def api_client(self) -> noctis_sdk.ApiClient:
        """Get the Noctis API client.
        
        Returns:
            Configured API client instance.
        """
        if self._api_client is None:
            self._api_client = noctis_sdk.ApiClient(
                configuration=noctis_sdk.Configuration(
                    access_token=self.api_key
                )
            )
        return self._api_client
    
    @property
    def domains_api(self) -> noctis_sdk.DomainsApi:
        """Get the Noctis domains API client.
        
        Returns:
            Configured domains API client instance.
        """
        if self._domains_api is None:
            self._domains_api = noctis_sdk.DomainsApi(self.api_client)
        return self._domains_api
    
    @property
    def asns_api(self) -> noctis_sdk.AsnsApi:
        """Get the Noctis ASNs API client.
        
        Returns:
            Configured ASNs API client instance.
        """
        if self._asns_api is None:
            self._asns_api = noctis_sdk.AsnsApi(self.api_client)
        return self._asns_api 