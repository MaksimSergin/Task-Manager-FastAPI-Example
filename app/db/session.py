# app/db/session.py

import asyncpg
from app.core.config import settings

class Database:
    def __init__(self):
        self.pool: asyncpg.pool.Pool = None

    async def connect(self):
        """Establishes a connection pool to the PostgreSQL database."""
        try:
            self.pool = await asyncpg.create_pool(dsn=settings.DATABASE_URL)
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            raise

    async def disconnect(self):
        """Closes the connection pool."""
        if self.pool:
            await self.pool.close()

    async def fetch(self, query: str, *args):
        """Fetches multiple records from the database."""
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def fetchrow(self, query: str, *args):
        """Fetches a single record from the database."""
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    async def execute(self, query: str, *args):
        """Executes a command (INSERT, UPDATE, DELETE) in the database."""
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)

# Initialize the Database instance
db = Database()

async def init_models():
    """Creates database tables if they do not exist."""
    try:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(128) NOT NULL
        );
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description VARCHAR(255),
            status VARCHAR(50) DEFAULT 'in_progress' NOT NULL,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
        );
        """)
    except Exception as e:
        print(f"Error initializing models: {e}")
        raise
