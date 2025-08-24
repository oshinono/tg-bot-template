from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from redis.asyncio import from_url
from config import settings
import json
from datetime import datetime
from consts import DATETIME_PATTERN

DB_URL = settings.postgres_url
REDIS_URL = settings.redis_url

engine = create_async_engine(DB_URL, pool_size=20, max_overflow=50, pool_timeout=30)

async_session_maker = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

class Base(DeclarativeBase):
    def __getattribute__(self, name):
        value = super().__getattribute__(name)
        if name in ('created_at', 'updated_at', 'date') and isinstance(value, datetime):
            return value.strftime(DATETIME_PATTERN)
        return value

class RedisClient:
    def __init__(self):
        self._redis_client = from_url(url=REDIS_URL, decode_responses=True)

    async def get_by_pattern(self, pattern: str) -> list[dict | None]:
        keys = await self._redis_client.keys(pattern)
        if not keys:
            return []
        values = await self._redis_client.mget(*keys)
        return [json.loads(value) if value else None for value in values]
    
    async def get(self, key: str) -> dict | None:
        value = await self._redis_client.get(key)
        return json.loads(value) if value else None
    
    async def set(self, key: str, value: dict, ttl: int | None = None) -> None:
        await self._redis_client.set(key, json.dumps(value), ex=ttl)
        
    async def delete(self, key: str) -> None:
        await self._redis_client.delete(key)