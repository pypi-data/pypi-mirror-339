"""NoctisRetriever retrievers."""

import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional, Set

import noctis_sdk
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from langchain_noctis.config import NoctisConfig
from langchain_noctis.registry import InfoSourceRegistry
from langchain_noctis.sources.enums import InfoType

# Set up logging
logger = logging.getLogger(__name__)


class NoctisRetriever(BaseRetriever):
    """Noctis retriever for domain information.
    
    This retriever extracts domain names from a query and fetches domain information
    for each detected domain using the Noctis API. It returns a separate document
    for each domain found, including both general domain information and mail server
    information if available.
    """

    k: int = 3
    parallel_requests: bool = True
    max_workers: int = 5
    
    # Information source configuration
    source_registry: Optional[InfoSourceRegistry] = None
    
    # Source limits configuration
    source_limits: Dict[str, int] = {
        InfoType.ORGANIZATION_DOMAINS: 25,
        InfoType.IP_SHARING_DOMAINS: 25,
        InfoType.NETWORK_PREFIX_DOMAINS: 25
    }

    def __init__(
        self, 
        api_client: Optional[noctis_sdk.ApiClient] = None,
        domains_api: Optional[noctis_sdk.DomainsApi] = None,
        source_registry: Optional[InfoSourceRegistry] = None,
        **kwargs: Any
    ):
        """Initialize the NoctisRetriever.
        
        Args:
            api_client: Optional API client to use
            domains_api: Optional domains API client to use
            source_registry: Optional source registry to use
            **kwargs: Additional keyword arguments
        """
        super().__init__(**kwargs)
        
        # Set up configuration
        self._config = NoctisConfig()
        
        # Get domains API from config or use provided one
        domains_api = domains_api or self._config.domains_api
            
        # Set up source registry if not provided
        self.source_registry = source_registry or InfoSourceRegistry(domains_api)
        
        # Handle specific limit parameters
        if "network_prefix_domains_limit" in kwargs:
            self.source_limits[InfoType.NETWORK_PREFIX_DOMAINS] = (
                kwargs["network_prefix_domains_limit"]
            )
            
        if "organization_domains_limit" in kwargs:
            org_limit = kwargs["organization_domains_limit"]
            self.source_limits[InfoType.ORGANIZATION_DOMAINS] = org_limit
            
        if "ip_sharing_domains_limit" in kwargs:
            ip_limit = kwargs["ip_sharing_domains_limit"]
            self.source_limits[InfoType.IP_SHARING_DOMAINS] = ip_limit
        
        # Configure enabled sources
        self._configure_enabled_sources(kwargs)
        
        # Apply custom source limits to any sources that were already enabled or created
        for source_name, limit in self.source_limits.items():
            # Convert enum to string for registry lookup
            is_enum = isinstance(source_name, InfoType)
            source_name_str = source_name.value if is_enum else source_name
            
            # If the source is in the registry, apply the custom limit
            source = self.source_registry.get_source(source_name_str)
            if source is not None and hasattr(source, 'limit'):
                # Create a new source with our custom limit
                new_source = source.__class__(source.domains_api, limit=limit)
                # Register the new source
                self.source_registry.register_source(source_name_str, new_source)

    def _configure_enabled_sources(self, kwargs: Dict[str, Any]) -> None:
        """Configure which sources are enabled based on kwargs.
        
        Args:
            kwargs: The kwargs passed to the constructor.
        """
        # Source configuration mapping (source_type, kwarg_name, default_value)
        source_configs = [
            (InfoType.MAIL_SERVERS, "include_mail_servers", True),
            (InfoType.ORGANIZATION_DOMAINS, "include_organization_domains", False),
            (InfoType.IP_SHARING_DOMAINS, "include_ip_sharing_domains", False),
            (InfoType.NETWORK_PREFIX_DOMAINS, "include_network_prefix_domains", False),
            (InfoType.DOMAIN_NAME_SERVERS, "include_domain_name_servers", False)
        ]
        
        # Process each source configuration
        for source_name, kwarg_name, default_value in source_configs:
            source_enabled = kwargs.get(kwarg_name, default_value)
            source_already_enabled = source_name in self.source_registry.enabled_sources
            
            if source_enabled and not source_already_enabled:
                # Enable the source first
                self.source_registry.enable_source(source_name)
                
                # If this is a source with a custom limit, apply it
                if source_name in self.source_limits:
                    # Re-apply our custom limit after enabling
                    self.set_source_limit(source_name, self.source_limits[source_name])
            elif not source_enabled and source_already_enabled:
                self.source_registry.disable_source(source_name)

    def _configure_source_limits(self, kwargs: Dict[str, Any] = None) -> None:
        """Configure source-specific limits.
        
        Args:
            kwargs: Optional keyword arguments that may contain limit overrides
        """
        if kwargs is None:
            kwargs = {}
            
        # Update source limits from kwargs
        for source_name, default_limit in self.source_limits.items():
            limit_attr = f"{source_name}_limit"
            new_limit = kwargs.get(limit_attr, default_limit)
            
            # Set the limit for this source
            self.set_source_limit(source_name, new_limit)

    def set_source_limit(self, source_name: str, limit: int) -> None:
        """Set a custom limit for a specific source.
        
        Args:
            source_name: The name of the source to set the limit for
            limit: The new limit value
        """
        # Store the limit in the source_limits dictionary
        if isinstance(source_name, InfoType):
            self.source_limits[source_name] = limit
            # For registry lookup, we need the string value
            source_name_str = source_name.value
        else:
            # Find the InfoType enum for this source name if it exists
            for info_type in self.source_limits.keys():
                if info_type.value == source_name:
                    self.source_limits[info_type] = limit
                    source_name_str = source_name
                    break
            else:
                # Not found in enum keys, use as is
                source_name_str = source_name
        
        # Get the source if it exists
        source = self.source_registry.get_source(source_name_str)
        if source is not None and hasattr(source, 'limit'):
            # Create a new source with the updated limit
            new_source = source.__class__(source.domains_api, limit=limit)
            # Register the new source
            self.source_registry.register_source(source_name_str, new_source)

    def _extract_domains(self, text: str) -> List[str]:
        """
        Extract domain names from text.
        
        Args:
            text: The text to extract domain names from.
            
        Returns:
            List of extracted domain names.
        """
        # This regex will match common domain patterns
        domain_pattern = (
            r'(?:https?:\/\/)?(?:www\.)?([a-zA-Z0-9][-a-zA-Z0-9]{0,62}'
            r'(?:\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+)'
        )
        
        # Find all matches and extract the domain part (group 1)
        domains = re.findall(domain_pattern, text)
        
        # Remove duplicates while preserving order
        unique_domains: Set[str] = set()
        result = []
        
        for domain in domains:
            if domain not in unique_domains:
                unique_domains.add(domain)
                result.append(domain)
        
        # If no domains were found, try to use the entire query as a domain
        if not result and self._is_potential_domain(text):
            result.append(text.strip())
            
        return result
    
    def _is_potential_domain(self, text: str) -> bool:
        """
        Check if a string could potentially be a domain name.
        
        Args:
            text: The string to check.
            
        Returns:
            True if the string could be a domain name, False otherwise.
        """
        # Check if the text contains at least one dot and no spaces
        return '.' in text and ' ' not in text.strip()

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun, **kwargs: Any
    ) -> List[Document]:
        """
        Extract domains from query and get domain information from Noctis API.

        Args:
            query: The text to extract domains from and query information for.
            run_manager: The callback manager for the retriever run.
            **kwargs: Additional arguments.

        Returns:
            A list of documents containing domain information, one per detected domain.
        """
        k = kwargs.get("k", self.k)
        enabled_sources = kwargs.get(
            "enabled_sources", self.source_registry.enabled_sources
        )
        
        # Debug logging for settings
        logger.debug(
            f"NoctisRetriever settings - k: {k}, enabled_sources: {enabled_sources}"
        )
        
        documents = []
        
        # Extract domains from the query
        domains = self._extract_domains(query)
        logger.info(f"Extracted domains: {domains}")
        
        # If no domains were found, return empty document(s)
        if not domains:
            documents.append(Document(
                page_content=f"No valid domains found in query: {query}",
                metadata={"query": query, "error": "no_domains_found"}
            ))
            return documents[:k]
        
        # Process domains with the appropriate method
        if self.parallel_requests and len(domains) > 1:
            documents = self._process_domains_parallel(
                domains, enabled_sources, **kwargs
            )
        else:
            documents = self._process_domains_sequential(
                domains, enabled_sources, **kwargs
            )
        
        # Ensure we have at most k documents
        if len(documents) > k:
            documents = documents[:k]
        elif len(documents) < k and documents:
            # Fill with duplicates if needed
            documents = self._fill_with_empty_docs(documents, k)
            
        return documents

    def _create_error_document(self, domain: str, exception: Exception) -> Document:
        """
        Create an error document for a domain processing error.
        
        Args:
            domain: The domain that caused the error.
            exception: The exception that occurred.
            
        Returns:
            A Document describing the error.
        """
        error_msg = f"Exception when processing domain {domain}: {str(exception)}"
        logger.exception(error_msg)
        return Document(
            page_content=error_msg,
            metadata={"error": str(exception), "domain": domain}
        )

    def _process_domains_parallel(
        self, domains: List[str], enabled_sources: List[str], **kwargs: Any
    ) -> List[Document]:
        """
        Process multiple domains in parallel.
        
        Args:
            domains: List of domains to process.
            enabled_sources: List of enabled source types.
            **kwargs: Additional arguments.
            
        Returns:
            List of documents with domain information.
        """
        documents = []
        max_workers = min(self.max_workers, len(domains))
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all domain processing tasks
            future_to_domain = {
                executor.submit(
                    self._process_domain, domain, enabled_sources, **kwargs
                ): domain for domain in domains
            }
            
            # Process results as they complete
            for future in as_completed(future_to_domain):
                domain = future_to_domain[future]
                try:
                    domain_docs = future.result()
                    documents.extend(domain_docs)
                except Exception as e:
                    documents.append(self._create_error_document(domain, e))
                    
        return documents

    def _process_domains_sequential(
        self, domains: List[str], enabled_sources: List[str], **kwargs: Any
    ) -> List[Document]:
        """
        Process multiple domains sequentially.
        
        Args:
            domains: List of domains to process.
            enabled_sources: List of enabled source types.
            **kwargs: Additional arguments.
            
        Returns:
            List of documents with domain information.
        """
        documents = []
        
        for domain in domains:
            try:
                domain_docs = self._process_domain(domain, enabled_sources, **kwargs)
                documents.extend(domain_docs)
            except Exception as e:
                documents.append(self._create_error_document(domain, e))
                
        return documents

    def _process_domain(
        self, domain: str, enabled_sources: List[str], **kwargs: Any
    ) -> List[Document]:
        """
        Process a single domain with all enabled sources.
        
        Args:
            domain: The domain to process.
            enabled_sources: List of enabled source types.
            **kwargs: Additional arguments.
            
        Returns:
            List of documents with domain information.
        """
        documents = []
        
        # Apply custom source limits if provided in kwargs
        source_limits = {}
        for source_name in self.source_limits:
            limit_kwarg = f"{source_name}_limit"
            if limit_kwarg in kwargs:
                source_limits[source_name] = kwargs[limit_kwarg]
        
        # Process each enabled source
        for source_name in enabled_sources:
            source = self.source_registry.get_source(source_name)
            
            if source is not None:
                # Apply any custom limits for this source
                source_kwargs = {}
                if source_name in source_limits:
                    source_kwargs["limit"] = source_limits[source_name]
                
                try:
                    # Process the domain with this source
                    document = source.process(domain, **source_kwargs)
                    if document:
                        documents.append(document)
                except Exception as e:
                    logger.warning(
                        f"Error processing {domain} with {source_name}: {str(e)}"
                    )
                    # Skip failed sources, don't add error documents for them
        
        # If no documents were generated, create a fallback document
        if not documents:
            documents.append(Document(
                page_content=f"No information found for domain: {domain}",
                metadata={"domain": domain, "error": "no_information_found"}
            ))
            
        return documents

    def _fill_with_empty_docs(
        self, 
        documents: List[Document], 
        target_count: int
    ) -> List[Document]:
        """
        Fill the document list to reach target_count by duplicating the first document.
        
        Args:
            documents: Current list of documents.
            target_count: Desired document count.
            
        Returns:
            Expanded list of documents.
        """
        if not documents or len(documents) >= target_count:
            return documents
            
        # Copy the first document for padding
        result = documents.copy()
        first_doc = documents[0]
        
        # Add duplicates until we reach the target count
        while len(result) < target_count:
            result.append(Document(
                page_content=first_doc.page_content,
                metadata={**first_doc.metadata, "is_duplicate": True}
            ))
            
        return result