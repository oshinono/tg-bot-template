import asyncio
from aiogram import Bot, Dispatcher
from consts import ALLOWED_UPDATES
from cmnds import commands
from loguru import logger
from utils import setup_logger, setup_schedule
from sqlalchemy.ext.asyncio import AsyncSession

from providers import container
from router import router as index_router

from middlewares import ClientMiddleware
from database import REDIS_URL, RedisClient
from aiogram.fsm.storage.redis import RedisStorage


async def init():
    setup_logger("bot")
    async with container() as c:
        # session = await c.get(AsyncSession)
        redis = await c.get(RedisClient)
        await setup_schedule(redis)


async def main():
    await init()

    async with container() as c:
        bot = await c.get(Bot)
        redis = await c.get(RedisClient)
        psql_session = await c.get(AsyncSession)

        await bot.set_my_commands(commands)
        await bot.delete_webhook(drop_pending_updates=True)

        try:
            storage = RedisStorage.from_url(REDIS_URL)
            dp: Dispatcher = Dispatcher(storage=storage)
            dp.include_routers(index_router)

            dp.update.middleware.register(
                ClientMiddleware(redis=redis, session=psql_session)
            )

            bot_info = await bot.get_me()
            logger.info(f"Бот запущен | {bot_info.full_name}, @{bot_info.username}")

            await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
        finally:
            await dp.stop_polling()
            await dp.storage.close()
            await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
