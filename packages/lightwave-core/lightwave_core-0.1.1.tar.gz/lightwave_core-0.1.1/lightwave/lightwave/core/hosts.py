"""
Django Hosts configuration for Lightwave Ecosystem.

This file defines the host patterns for subdomain routing using django-hosts.
It loads configuration from lightwave-config/django-hosts-config.yaml.
"""

import os
import yaml
from django.conf import settings
from django_hosts import patterns, host

# Path to the configuration file
CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
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
config = load_config()

# Get current application from settings or environment
def get_current_application():
    """Determine which application is currently running."""
    app_name = getattr(settings, 'LIGHTWAVE_APPLICATION', os.environ.get('LIGHTWAVE_APPLICATION', 'createos'))
    return app_name

# Get application configuration
def get_application_config():
    """Get configuration for the current application."""
    app_name = get_current_application()
    app_config = config['applications'].get(app_name)
    if not app_config:
        raise RuntimeError(f"No configuration found for application: {app_name}")
    return app_config

# Dynamic host patterns based on configuration
def get_host_patterns():
    """Generate host patterns based on the configuration."""
    app_config = get_application_config()
    host_patterns = []
    
    # Add default host
    default_host = app_config.get('default_host', 'app')
    host_patterns.append(
        host(r'', settings.ROOT_URLCONF, name=default_host)
    )
    
    # Add subdomains
    for subdomain in app_config.get('enabled_subdomains', []):
        subdomain_config = config['common_subdomains'].get(subdomain)
        if not subdomain_config:
            continue
            
        urls_module = subdomain_config.get('urls_module', f'{subdomain}_urls')
        host_conf_name = subdomain_config.get('host_conf_name', f'{subdomain}_host')
        
        # Full module path assuming urls are in lightwave.core.[app].urls.[subdomain]_urls
        urls_module_path = f"lightwave.core.{get_current_application()}.urls.{urls_module}"
        
        # Add to patterns
        host_patterns.append(
            host(r'^{0}$'.format(subdomain), urls_module_path, name=host_conf_name)
        )
    
    return host_patterns

# Create patterns for django-hosts
host_patterns = patterns('',
    *get_host_patterns()
) 