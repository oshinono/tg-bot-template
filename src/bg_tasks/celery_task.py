import asyncio
from bg_tasks.celery_app import app
from bg_tasks.schemas import BaseCeleryTaskData, BaseCeleryTaskReslt
from loguru import logger
from bg_tasks.utils import send_report_of_scanning, get_short_statistics

@app.task
def celery_task(data: dict = None):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        if data:
            return loop.run_until_complete(_async_task(data))
        else:
            return loop.run_until_complete(_async_task())
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        raise e

async def _async_task(validated_data: BaseCeleryTaskData = None):
    result = BaseCeleryTaskReslt()
    await send_report_of_scanning(result, validated_data)
    short_statistics = await get_short_statistics(result)
    return short_statistics

