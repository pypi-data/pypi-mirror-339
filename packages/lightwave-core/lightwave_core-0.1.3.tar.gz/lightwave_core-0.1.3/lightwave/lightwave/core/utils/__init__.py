"""Utility functions for the LightWave ecosystem."""

# Import and reexport common utilities here for easier imports
from .formatting import format_currency, format_date

# Import subdomain utilities to make them accessible via lightwave.core.utils
try:
    from .subdomain import (
        get_host_url,
        get_subdomain_list,
        is_subdomain_enabled,
        get_parent_domain,
        get_full_domain,
        get_current_subdomain,
    )
    
    # Update __all__ with subdomain utils when available
    __all__ = [
        "format_date", 
        "format_currency",
        "get_host_url",
        "get_subdomain_list",
        "is_subdomain_enabled",
        "get_parent_domain",
        "get_full_domain",
        "get_current_subdomain",
    ]
except ImportError:
    # Handle gracefully in environments without Django/django-hosts
    __all__ = ["format_date", "format_currency"]
