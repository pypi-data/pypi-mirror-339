"""NoctisRetriever retrievers."""

import logging
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional, Set

import noctis_sdk
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from langchain_noctis.registry import InfoSourceRegistry
from langchain_noctis.sources.base import DomainInfoSource
from langchain_noctis.sources.ip_sharing_domains import IPSharingDomainsSource
from langchain_noctis.sources.network_prefix_domains import NetworkPrefixDomainsSource
from langchain_noctis.sources.organization_domains import OrganizationDomainsSource

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
    api_client: Optional[noctis_sdk.ApiClient] = None
    domains_api: Optional[noctis_sdk.DomainsApi] = None
    parallel_requests: bool = True
    max_workers: int = 5
    
    # Information source configuration
    enabled_sources: List[str] = ["domain_info"]
    source_registry: Optional[InfoSourceRegistry] = None
    
    # Source-specific settings
    organization_domains_limit: int = 25
    ip_sharing_domains_limit: int = 25
    network_prefix_domains_limit: int = 25

    def __init__(self, **kwargs: Any):
        """Initialize the NoctisRetriever."""
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
            
        # Set up source registry
        if self.source_registry is None:
            self.source_registry = InfoSourceRegistry(self.domains_api)
        
        # Configure enabled sources based on kwargs
        self._configure_enabled_sources(kwargs)
        
        # Configure source limits
        self._configure_source_limits()

    def _configure_enabled_sources(self, kwargs: Dict[str, Any]) -> None:
        """Configure which sources are enabled based on kwargs.
        
        Args:
            kwargs: The kwargs passed to the constructor.
        """
        # For backward compatibility, add mail_servers by default
        if "mail_servers" not in self.enabled_sources and kwargs.get(
            "include_mail_servers", True
        ):
            self.enabled_sources.append("mail_servers")
        
        # Configure source enablement with simple pattern
        source_configs = [
            ("organization_domains", "include_organization_domains", False),
            ("ip_sharing_domains", "include_ip_sharing_domains", False),
            ("network_prefix_domains", "include_network_prefix_domains", False)
        ]
        
        for source_name, kwarg_name, default_value in source_configs:
            if (
                source_name not in self.enabled_sources 
                and kwargs.get(kwarg_name, default_value)
            ):
                self.enabled_sources.append(source_name)

    def _configure_source_limits(self) -> None:
        """Configure source-specific limits."""
        sources_with_limits = [
            (
                "organization_domains", 
                OrganizationDomainsSource, 
                self.organization_domains_limit
            ),
            (
                "ip_sharing_domains", 
                IPSharingDomainsSource, 
                self.ip_sharing_domains_limit
            ),
            (
                "network_prefix_domains", 
                NetworkPrefixDomainsSource, 
                self.network_prefix_domains_limit
            )
        ]
        
        for source_name, source_type, limit_value in sources_with_limits:
            source = self.source_registry.get_source(source_name)
            if isinstance(source, source_type):
                source.limit = limit_value

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
        enabled_sources = kwargs.get("enabled_sources", self.enabled_sources)
        
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
            for i in range(min(k, 1)):  # At least one document, but no more than k
                documents.append(Document(
                    page_content=f"No valid domains found in query: {query}",
                    metadata={"query": query, "error": "no_domains_found"}
                ))
            return documents
        
        # Get domain information for each domain
        if self.parallel_requests and len(domains) > 1:
            # Process domains in parallel
            documents = self._process_domains_parallel(
                domains, enabled_sources, **kwargs
            )
        else:
            # Process domains sequentially
            documents = self._process_domains_sequential(
                domains, enabled_sources, **kwargs
            )
        
        # Fill with duplicates if needed to meet k
        if k > len(documents) and documents:
            documents = self._fill_with_duplicates(documents, k)
        
        # Return at most k documents
        return documents[:k]
    
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
        """Process multiple domains in parallel and return documents."""
        documents = []
        
        with ThreadPoolExecutor(
            max_workers=min(self.max_workers, len(domains))
        ) as executor:
            future_to_domain = {
                executor.submit(
                    self._process_domain, domain, enabled_sources, **kwargs
                ): domain 
                for domain in domains
            }
            
            for future in as_completed(future_to_domain):
                domain = future_to_domain[future]
                try:
                    results = future.result()
                    documents.extend([doc for doc in results if doc])
                except Exception as exc:
                    documents.append(self._create_error_document(domain, exc))
                    
        return documents
    
    def _process_domains_sequential(
        self, domains: List[str], enabled_sources: List[str], **kwargs: Any
    ) -> List[Document]:
        """Process multiple domains sequentially and return documents."""
        documents = []
        
        for domain in domains:
            try:
                domain_docs = self._process_domain(domain, enabled_sources, **kwargs)
                documents.extend([doc for doc in domain_docs if doc])
            except Exception as exc:
                documents.append(self._create_error_document(domain, exc))
                
        return documents
    
    def _process_domain(
        self, domain: str, enabled_sources: List[str], **kwargs: Any
    ) -> List[Optional[Document]]:
        """
        Process a domain to get all requested information sources.
        
        Args:
            domain: The domain name to process.
            enabled_sources: List of information source names to process.
            
        Returns:
            A list of Documents with domain information from all sources.
        """
        results = []
        
        # Create source-specific kwargs mapping
        source_kwargs_mapping = {
            "organization_domains": {
                "limit": kwargs.get(
                    "organization_domains_limit", self.organization_domains_limit
                )
            },
            "ip_sharing_domains": {
                "limit": kwargs.get(
                    "ip_sharing_domains_limit", self.ip_sharing_domains_limit
                )
            },
            "network_prefix_domains": {
                "limit": kwargs.get(
                    "network_prefix_domains_limit", self.network_prefix_domains_limit
                )
            }
        }
        
        logger.debug(f"Processing domain {domain} with sources: {enabled_sources}")
        
        # Process each enabled information source
        for source_name in enabled_sources:
            source = self.source_registry.get_source(source_name)
            if source is not None:
                # Use source-specific kwargs if available, or empty dict otherwise
                source_specific_kwargs = source_kwargs_mapping.get(source_name, {})
                doc = source.process(domain, **source_specific_kwargs)
                if doc:
                    results.append(doc)
                    logger.debug(f"Added {source_name} document for {domain}")
            else:
                logger.warning(
                    f"Information source '{source_name}' not found in registry"
                )
        
        return results
    
    def _fill_with_duplicates(
        self, 
        documents: List[Document], 
        target_count: int
    ) -> List[Document]:
        """
        Fill the document list with duplicates to reach the target count.
        
        Args:
            documents: The original document list.
            target_count: The target number of documents.
            
        Returns:
            The document list filled with duplicates if needed.
        """
        if not documents or target_count <= len(documents):
            return documents
            
        original_count = len(documents)
        source_docs = documents.copy()
        
        for i in range(target_count - original_count):
            # Duplicate an existing document with a note that it's a duplicate
            idx = i % original_count
            original = source_docs[idx]
            domain = original.metadata.get("domain", "unknown")
            doc_type = original.metadata.get("document_type", "domain_info")
            
            dup_doc = Document(
                page_content=(
                    f"Additional result (duplicate of {domain} {doc_type}):\n"
                    f"{original.page_content}"
                ),
                metadata={
                    **original.metadata,
                    "duplicate": True,
                    "duplicate_of": domain,
                    "result_number": i + original_count + 1
                }
            )
            documents.append(dup_doc)
            
        return documents
            
    def add_info_source(
        self, 
        name: str, 
        source: DomainInfoSource, 
        enable: bool = True
    ) -> None:
        """
        Add a new information source to the retriever.
        
        Args:
            name: The name to register the source under.
            source: The information source to add.
            enable: Whether to enable the source by default.
        """
        if self.source_registry is not None:
            self.source_registry.register_source(name, source)
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
        if (
            self.source_registry is not None 
            and self.source_registry.get_source(name) is not None
        ):
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