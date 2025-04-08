"""Enums used across the source classes."""

from enum import Enum


class InfoType(str, Enum):
    """Information types provided by different sources."""
    
    DOMAIN_INFO = "domain_info"
    MAIL_SERVERS = "mail_servers"
    ORGANIZATION_DOMAINS = "organization_domains"
    IP_SHARING_DOMAINS = "ip_sharing_domains"
    NETWORK_PREFIX_DOMAINS = "network_prefix_domains"
    DOMAIN_NAME_SERVERS = "domain_name_servers" 