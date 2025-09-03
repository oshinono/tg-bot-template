from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import AsyncGenerator
from dishka import make_async_container

from consts import default_bot_settings

from database import RedisClient

from config import settings
from aiogram import Bot


class DbProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def provide_postgres(self) -> AsyncGenerator[AsyncSession, None]:
        async for session in get_async_session():
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @provide(scope=Scope.APP)
    async def provide_redis(self) -> RedisClient:
        return RedisClient()


class AiogramProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_bot(self) -> Bot:
        return Bot(token=settings.token, default=default_bot_settings)


container = make_async_container(DbProvider(), AiogramProvider())
