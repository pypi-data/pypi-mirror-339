import asyncio
import unittest
from unittest.mock import patch, MagicMock

import manaflow
from manaflow.connection import connection, Depends
from manaflow.secrets import secrets_manager


class TestConnection(unittest.TestCase):
    def setUp(self):
        from manaflow.connection import registry
        registry._connections = {}
        registry._connection_instances = {}
        registry._secret_keys = {}
        secrets_manager.clear()
        
    def test_connection_decorator(self):
        @connection("test_conn", secret_keys=["uri"])
        async def test_factory(uri):
            return f"Connected to {uri}"
        
        from manaflow.connection import registry
        self.assertIn("test_conn", registry._connections)
        self.assertEqual(registry._secret_keys["test_conn"], ["uri"])
        
    def test_get_connection(self):
        @connection("test_conn", secret_keys=["uri"])
        async def test_factory(uri):
            return f"Connected to {uri}"
        
        secrets_manager.set_secret("test_conn_uri", "test://localhost")
        
        from manaflow.connection import registry
        result = asyncio.run(registry.get_connection("test_conn"))
        self.assertEqual(result, "Connected to test://localhost")
        
    def test_depends(self):
        @connection("test_conn", secret_keys=["uri"])
        async def test_factory(uri):
            return f"Connected to {uri}"
        
        secrets_manager.set_secret("test_conn_uri", "test://localhost")
        
        async def test_function(conn=Depends("test_conn")):
            return await conn()
        
        result = asyncio.run(test_function())
        self.assertEqual(result, "Connected to test://localhost")
        
    def test_missing_secret(self):
        @connection("test_conn", secret_keys=["uri"])
        async def test_factory(uri):
            return f"Connected to {uri}"
        
        from manaflow.connection import registry
        with self.assertRaises(ValueError):
            asyncio.run(registry.get_connection("test_conn"))
            
    def test_close_connections(self):
        mock_conn = MagicMock()
        mock_conn.close = MagicMock()
        
        @connection("test_conn", secret_keys=[])
        async def test_factory():
            return mock_conn
        
        from manaflow.connection import registry, close_connections
        
        asyncio.run(registry.get_connection("test_conn"))
        
        asyncio.run(close_connections())
        
        mock_conn.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
