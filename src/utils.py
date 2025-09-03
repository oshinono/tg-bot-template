from loguru import logger
from sqlalchemy import TypeDecorator, DateTime
from datetime import datetime
from consts import CURRENT_TIMEZONE
import pytz
from aiogram.fsm.context import FSMContext

from bg_tasks.consts import INIT_SCHEDULE_TIME

from database import RedisClient


def setup_logger(log_name: str):
    logger.add(
        f"logs/{log_name}.log",
        format="{time} {level} {message}",
        level="DEBUG",
        rotation="10:00",
        retention="10 days",
        colorize=True,
        compression="zip",
    )


class TimestampType(TypeDecorator):
    impl = DateTime

    def process_bind_param(self, value, dialect):
        if isinstance(value, int):
            return datetime.fromtimestamp(value, pytz.timezone(CURRENT_TIMEZONE))
        return value


async def clear_state(state: FSMContext):
    keys_to_preserve = [
        # список ключей для сохранения
    ]

    current_data = await state.get_data()

    await state.clear()

    for key in keys_to_preserve:
        if key in current_data and current_data[key] is not None:
            await state.update_data({key: current_data[key]})


async def setup_schedule(redis: RedisClient):
    schedule_time = await redis.get("schedule_time")

    if schedule_time is None:
        from bg_tasks.celery_app import update_schedule

        default_time = INIT_SCHEDULE_TIME
        default_time_string = (
            f"{list(default_time.hour)[0]:02d}:{list(default_time.minute)[0]:02d}"
        )

        await redis.set("schedule_time", default_time_string)
        update_schedule("scan-posts", default_time)

        logger.info(f"Инициализировано время расписания: {default_time_string}")
    else:
        logger.info(f"Время расписания уже установлено: {schedule_time}")
