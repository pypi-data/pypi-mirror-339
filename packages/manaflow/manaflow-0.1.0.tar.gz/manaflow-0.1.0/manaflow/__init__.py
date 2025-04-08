"""
Manaflow Python client.

This module provides utilities for interacting with Manaflow services.
"""

from .connection import connection, Depends, close_connections
from .secrets import SecretsManager, secrets_manager

__version__ = "0.1.0"
