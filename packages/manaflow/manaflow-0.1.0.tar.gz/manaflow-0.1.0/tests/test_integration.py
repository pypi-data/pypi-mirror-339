import asyncio
import json
import os
import pytest
import tempfile
from unittest.mock import patch, MagicMock

import manaflow
from manaflow.secrets import secrets_manager
from manaflow.connection import connection, Depends, close_connections


class TestIntegration:
    def setup_method(self):
        from manaflow.connection import registry
        registry._connections = {}
        registry._connection_instances = {}
        registry._secret_keys = {}
        secrets_manager.clear()
        
    def teardown_method(self):
        from manaflow.connection import registry
        registry._connections = {}
        registry._connection_instances = {}
        registry._secret_keys = {}
        secrets_manager.clear()
    
    @pytest.mark.asyncio
    async def test_connection_with_individual_secrets(self):
        secrets_manager.set_secret("test_conn_uri", "test://localhost")
        secrets_manager.set_secret("test_conn_port", 5432)
        
        @connection("test_conn", secret_keys=["uri", "port"])
        async def test_factory(uri, port):
            return {"uri": uri, "port": port}
        
        async def test_function(conn=Depends("test_conn")):
            return await conn()
        
        result = await test_function()
        assert result["uri"] == "test://localhost"
        assert result["port"] == 5432
        
        await close_connections()
    
    @pytest.mark.asyncio
    async def test_connection_with_object_secrets(self):
        secrets_manager.set_secret("test_conn", {
            "uri": "test://localhost",
            "port": 5432
        })
        
        @connection("test_conn", secret_keys=["uri", "port"])
        async def test_factory(uri, port):
            return {"uri": uri, "port": port}
        
        async def test_function(conn=Depends("test_conn")):
            return await conn()
        
        result = await test_function()
        assert result["uri"] == "test://localhost"
        assert result["port"] == 5432
        
        await close_connections()
    
    @pytest.mark.asyncio
    async def test_load_secrets_from_file(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "test_conn": {
                    "uri": "test://localhost",
                    "port": 5432
                }
            }, f)
            temp_file = f.name
        
        try:
            secrets_manager.load_from_file(temp_file)
            
            @connection("test_conn", secret_keys=["uri", "port"])
            async def test_factory(uri, port):
                return {"uri": uri, "port": port}
            
            async def test_function(conn=Depends("test_conn")):
                return await conn()
            
            result = await test_function()
            assert result["uri"] == "test://localhost"
            assert result["port"] == 5432
            
            await close_connections()
        finally:
            os.unlink(temp_file)
    
    @pytest.mark.asyncio
    async def test_multiple_connections(self):
        secrets_manager.set_secret("postgres_conn", {
            "uri": "postgresql://user:pass@localhost/db"
        })
        secrets_manager.set_secret("redis_conn", {
            "uri": "redis://localhost:6379"
        })
        
        @connection("postgres_conn", secret_keys=["uri"])
        async def postgres_factory(uri):
            return {"type": "postgres", "uri": uri}
        
        @connection("redis_conn", secret_keys=["uri"])
        async def redis_factory(uri):
            return {"type": "redis", "uri": uri}
        
        async def postgres_function(conn=Depends("postgres_conn")):
            return await conn()
        
        async def redis_function(conn=Depends("redis_conn")):
            return await conn()
        
        postgres_result = await postgres_function()
        redis_result = await redis_function()
        
        assert postgres_result["type"] == "postgres"
        assert postgres_result["uri"] == "postgresql://user:pass@localhost/db"
        assert redis_result["type"] == "redis"
        assert redis_result["uri"] == "redis://localhost:6379"
        
        await close_connections()
