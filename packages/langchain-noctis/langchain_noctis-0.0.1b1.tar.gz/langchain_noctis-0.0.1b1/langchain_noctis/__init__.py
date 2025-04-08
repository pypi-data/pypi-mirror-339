"""
LangChain Noctis API Integration.

Provides tools to integrate with Noctis API, including retrievers for domain information
and other domain-related tools.
"""

from importlib import metadata

from langchain_noctis.registry import InfoSourceRegistry
from langchain_noctis.retrievers import NoctisRetriever
from langchain_noctis.sources import (
    DomainBasicInfoSource,
    DomainInfoSource,
    IPSharingDomainsSource,
    MailServerInfoSource,
    OrganizationDomainsSource,
)
from langchain_noctis.tools import NoctisTool

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = "0.1.1"  # Updated version with mail server support
del metadata  # optional, avoids polluting the results of dir(__package__)

__all__ = [
    "NoctisRetriever",
    "DomainInfoSource",
    "DomainBasicInfoSource",
    "MailServerInfoSource",
    "OrganizationDomainsSource",
    "IPSharingDomainsSource",
    "InfoSourceRegistry",
    "NoctisTool",
    "__version__",
]
