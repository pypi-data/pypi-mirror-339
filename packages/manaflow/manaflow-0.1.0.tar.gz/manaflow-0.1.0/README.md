# Manaflow

Async connection management for Manaflow services. This package provides utilities for managing database connections and other services with dependency injection.

## Installation

```bash
pip install manaflow
```

## Usage

```python
import asyncio
import manaflow
from manaflow import secrets_manager

# Pre-populate secrets manager with scoped keys
secrets_manager.set_secret("postgres_conn_db_uri", "postgresql://user:pass@localhost/mydb")
secrets_manager.set_secret("redis_conn_cache_uri", "redis://localhost:6379")

# Define connection factories with scoped secrets
@manaflow.connection("postgres_conn_db", secret_keys=["uri"])
async def postgres_factory(uri: str):
    # Use your preferred async PostgreSQL driver
    return await create_postgres_pool(uri)

@manaflow.connection("redis_conn_cache", secret_keys=["uri"])
async def redis_factory(uri: str):
    # Use your preferred async Redis driver
    return await create_redis_connection(uri)

# Use connections with dependency injection
async def demo_postgres(db=manaflow.Depends("postgres_conn_db")):
    # The connection is automatically retrieved and injected
    connection = await db()
    # Use the connection
    return {"status": "success"}

# Run everything
async def main():
    result = await demo_postgres()
    print(result)
    # Close all connections when done
    await manaflow.connection.close_connections()

if __name__ == "__main__":
    asyncio.run(main())
```

## Features

- Async connection management with dependency injection
- Secret management for connection credentials
- Support for multiple connection types (PostgreSQL, MySQL, MongoDB, Redis, HTTP, etc.)
- No external dependencies required

## License

MIT
