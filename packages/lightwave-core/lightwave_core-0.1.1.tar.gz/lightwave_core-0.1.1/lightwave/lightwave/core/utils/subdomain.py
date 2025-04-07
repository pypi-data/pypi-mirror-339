"""
Subdomain utilities for Lightwave Ecosystem.

This module provides helper functions for working with subdomains in the Lightwave ecosystem.
"""

import os
import yaml
from django.conf import settings
from django_hosts.resolvers import reverse as hosts_reverse

# Path to the configuration file
CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
    "lightwave-config", 
    "django-hosts-config.yaml"
)

def load_config():
    """Load configuration from YAML file."""
    try:
        with open(CONFIG_PATH, 'r') as config_file:
            return yaml.safe_load(config_file)
    except Exception as e:
        raise RuntimeError(f"Failed to load django-hosts configuration: {e}")

# Load configuration
config = None
try:
    config = load_config()
except Exception:
    # Handle gracefully in non-Django contexts
    pass

def get_application_name():
    """
    Get the current application name.
    
    Returns the application name from settings or environment.
    """
    if hasattr(settings, 'LIGHTWAVE_APPLICATION'):
        return settings.LIGHTWAVE_APPLICATION
    return os.environ.get('LIGHTWAVE_APPLICATION', 'createos')

def get_host_url(view_name, subdomain, scheme=None, kwargs=None, current_app=None):
    """
    Generate a URL for a specific subdomain and view.
    
    Args:
        view_name (str): The name of the view to reverse
        subdomain (str): The subdomain name (e.g., 'api', 'admin')
        scheme (str, optional): URL scheme (http, https)
        kwargs (dict, optional): URL parameters
        current_app (str, optional): Current application
        
    Returns:
        str: The full URL for the given view on the specified subdomain
    """
    if config is None:
        raise RuntimeError("Django hosts configuration not loaded")
    
    app_name = get_application_name()
    app_config = config['applications'].get(app_name)
    
    if not app_config:
        raise ValueError(f"No configuration found for application: {app_name}")
    
    # Get the host configuration name
    host_name = None
    for sd_name, sd_config in config['common_subdomains'].items():
        if sd_name == subdomain:
            host_name = sd_config.get('host_conf_name', f'{subdomain}_host')
            break
    
    if not host_name:
        if subdomain == app_config.get('default_host', 'app'):
            host_name = subdomain
        else:
            raise ValueError(f"No configuration found for subdomain: {subdomain}")
    
    # Generate the URL
    return hosts_reverse(view_name, host=host_name, kwargs=kwargs, scheme=scheme, current_app=current_app)

def get_subdomain_list():
    """
    Get a list of all enabled subdomains for the current application.
    
    Returns:
        list: A list of subdomain names that are enabled for the current application
    """
    if config is None:
        raise RuntimeError("Django hosts configuration not loaded")
    
    app_name = get_application_name()
    app_config = config['applications'].get(app_name)
    
    if not app_config:
        raise ValueError(f"No configuration found for application: {app_name}")
    
    return app_config.get('enabled_subdomains', [])

def is_subdomain_enabled(subdomain):
    """
    Check if a subdomain is enabled for the current application.
    
    Args:
        subdomain (str): The subdomain name to check
        
    Returns:
        bool: True if the subdomain is enabled, False otherwise
    """
    return subdomain in get_subdomain_list()

def get_parent_domain():
    """
    Get the parent domain for the current application.
    
    Returns:
        str: The parent domain name
    """
    if config is None:
        raise RuntimeError("Django hosts configuration not loaded")
    
    app_name = get_application_name()
    app_config = config['applications'].get(app_name)
    
    if not app_config:
        raise ValueError(f"No configuration found for application: {app_name}")
    
    return app_config.get('parent_host', '')

def get_full_domain(subdomain=None):
    """
    Get the full domain for a subdomain.
    
    Args:
        subdomain (str, optional): The subdomain name. If None, returns the parent domain.
        
    Returns:
        str: The full domain name (subdomain.parentdomain.tld)
    """
    parent = get_parent_domain()
    
    if not subdomain:
        return parent
    
    return f"{subdomain}.{parent}"

def get_current_subdomain(request):
    """
    Get the current subdomain from a request.
    
    Args:
        request: The Django request object
        
    Returns:
        str: The current subdomain name or None if not a subdomain
    """
    if not hasattr(request, 'get_host'):
        return None
    
    host = request.get_host()
    parent = get_parent_domain()
    
    # Check if it's a subdomain
    if not parent or not host.endswith(parent):
        return None
    
    # Extract the subdomain
    subdomain = host[:-len(parent)-1]  # Remove parent domain and the dot
    if not subdomain:
        return None
    
    return subdomain 