import asyncio
import functools
import inspect
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union, cast

from .secrets import secrets_manager

T = TypeVar('T')
ConnectionFactory = Callable[..., Any]
ConnectionType = TypeVar('ConnectionType')


class ConnectionRegistry:
    """Registry for connection factories."""
    
    _instance = None
    _connections: Dict[str, ConnectionFactory] = {}
    _connection_instances: Dict[str, Any] = {}
    _secret_keys: Dict[str, List[str]] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConnectionRegistry, cls).__new__(cls)
        return cls._instance
    
    def register(self, name: str, factory: ConnectionFactory, secret_keys: List[str]) -> None:
        """Register a connection factory."""
        self._connections[name] = factory
        self._secret_keys[name] = secret_keys
    
    async def get_connection(self, name: str) -> Any:
        """Get or create a connection instance."""
        if name not in self._connection_instances:
            if name not in self._connections:
                raise ValueError(f"Connection '{name}' not registered")
            
            factory = self._connections[name]
            secret_keys = self._secret_keys.get(name, [])
            
            kwargs = {}
            
            secret_obj = secrets_manager.get_secret(name)
            if secret_obj and isinstance(secret_obj, dict):
                for key in secret_keys:
                    if key in secret_obj:
                        kwargs[key] = secret_obj[key]
                    else:
                        secret_name = f"{name}_{key}"
                        secret_value = secrets_manager.get_secret(secret_name)
                        if secret_value is None:
                            raise ValueError(f"Secret '{key}' not found in '{name}' object or as '{secret_name}'")
                        kwargs[key] = secret_value
            else:
                for key in secret_keys:
                    secret_name = f"{name}_{key}"
                    secret_value = secrets_manager.get_secret(secret_name)
                    if secret_value is None:
                        raise ValueError(f"Secret '{secret_name}' not found")
                    kwargs[key] = secret_value
            
            self._connection_instances[name] = await factory(**kwargs)
        
        return self._connection_instances[name]
    
    async def close_all(self) -> None:
        """Close all connections."""
        for name, conn in self._connection_instances.items():
            if hasattr(conn, 'close'):
                if inspect.iscoroutinefunction(conn.close):
                    await conn.close()
                else:
                    conn.close()
            elif hasattr(conn, 'terminate'):
                if inspect.iscoroutinefunction(conn.terminate):
                    await conn.terminate()
                else:
                    conn.terminate()
        self._connection_instances.clear()


registry = ConnectionRegistry()


def connection(name: str, secret_keys: Optional[List[str]] = None):
    """
    Decorator to register a connection factory.
    
    Args:
        name: The name of the connection
        secret_keys: List of secret keys to retrieve from the secrets manager
    """
    def decorator(factory: ConnectionFactory) -> ConnectionFactory:
        registry.register(name, factory, secret_keys or [])
        return factory
    return decorator


class Depends:
    """
    Dependency injection for connections.
    
    Usage:
        async def my_function(db=Depends("my_connection")):
    """
    
    def __init__(self, connection_name: str):
        self.connection_name = connection_name
    
    def __call__(self) -> Any:
        return registry.get_connection(self.connection_name)


async def close_connections() -> None:
    """Close all connections."""
    await registry.close_all()
