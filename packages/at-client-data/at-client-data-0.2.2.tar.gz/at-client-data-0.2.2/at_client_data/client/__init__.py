"""
Client package for interacting with API endpoints.
"""
from .core import CoreClient
from .external import ExternalClient

__all__ = ["CoreClient", "ExternalClient"] 