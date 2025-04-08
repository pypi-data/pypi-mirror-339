import asyncio
import json
import os
import pytest
import tempfile
from unittest.mock import patch, MagicMock

import manaflow
from manaflow.secrets import secrets_manager, SecretsManager
from manaflow.connection import connection, Depends, close_connections


class TestManaflowJson:
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
        
        if os.path.exists("manaflow.json"):
            os.remove("manaflow.json")
    
    def test_create_manaflow_json(self):
        config = {
            "postgres_conn_db": {
                "uri": "postgresql://user:pass@localhost/mydb"
            },
            "mysql_conn_main": {
                "host": "localhost",
                "user": "root",
                "password": "pass",
                "db": "mydb"
            }
        }
        
        with open("manaflow.json", "w") as f:
            json.dump(config, f, indent=2)
        
        assert os.path.exists("manaflow.json")
        
        with open("manaflow.json", "r") as f:
            loaded_config = json.load(f)
        
        assert loaded_config == config
    
    def test_load_from_manaflow_json(self):
        config = {
            "postgres_conn_db": {
                "uri": "postgresql://user:pass@localhost/mydb"
            },
            "mysql_conn_main": {
                "host": "localhost",
                "user": "root",
                "password": "pass",
                "db": "mydb"
            }
        }
        
        with open("manaflow.json", "w") as f:
            json.dump(config, f, indent=2)
        
        new_manager = SecretsManager()
        
        assert new_manager.get_secret("postgres_conn_db") == {"uri": "postgresql://user:pass@localhost/mydb"}
        assert new_manager.get_secret("mysql_conn_main") == {
            "host": "localhost",
            "user": "root",
            "password": "pass",
            "db": "mydb"
        }
    
    @pytest.mark.asyncio
    async def test_connection_with_manaflow_json(self):
        config = {
            "test_conn": {
                "uri": "test://localhost",
                "port": 5432
            }
        }
        
        with open("manaflow.json", "w") as f:
            json.dump(config, f, indent=2)
        
        secrets_manager.clear()
        secrets_manager.load_from_file("manaflow.json")
        
        @connection("test_conn", secret_keys=["uri", "port"])
        async def test_factory(uri, port):
            return {"uri": uri, "port": port}
        
        async def test_function(conn=Depends("test_conn")):
            return await conn()
        
        result = await test_function()
        assert result["uri"] == "test://localhost"
        assert result["port"] == 5432
        
        await close_connections()
    
    def test_save_to_manaflow_json(self):
        secrets_manager.set_secret("postgres_conn_db", {
            "uri": "postgresql://user:pass@localhost/mydb"
        })
        secrets_manager.set_secret("mysql_conn_main", {
            "host": "localhost",
            "user": "root",
            "password": "pass",
            "db": "mydb"
        })
        
        secrets_manager.save_to_file("manaflow.json")
        
        assert os.path.exists("manaflow.json")
        
        with open("manaflow.json", "r") as f:
            loaded_config = json.load(f)
        
        assert loaded_config["postgres_conn_db"] == {"uri": "postgresql://user:pass@localhost/mydb"}
        assert loaded_config["mysql_conn_main"] == {
            "host": "localhost",
            "user": "root",
            "password": "pass",
            "db": "mydb"
        }
