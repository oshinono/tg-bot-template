import asyncio
import csv
import os
from datetime import datetime
from typing import Optional
from aiogram import Bot
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from bg_tasks.schemas import BaseCeleryTaskReslt, BaseCeleryTaskData
from providers import container
from users.service import UserService


async def prepare_text_to_csv(result: BaseCeleryTaskReslt) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"temp/scan_{timestamp}.csv"

    csv_columns = []

    os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
    with open(csv_filename, "w", encoding="utf-8-sig", newline="") as csvfile:
        writer = csv.writer(csvfile, dialect="excel")
        writer.writerow(csv_columns)

        # заполнить нужные строки

    return csv_filename


async def send_report_of_scanning(
    result: BaseCeleryTaskReslt, data: Optional[BaseCeleryTaskData] = None
):
    # media = []
    report_text = "<b>Обход</b>\n\n"

    async with container() as c:
        session: AsyncSession = await c.get(AsyncSession)
        bot = await c.get(Bot)

        if data:
            report_text += ""
            try:
                await bot.send_message(
                    chat_id=data.initiator_id, text=report_text
                )
            except Exception as e:
                logger.error(
                    f"Ошибка отправки отчета инициатору {data.initiator_id}: {e}"
                )
        else:
            report_text += ""
            users_to_send = await UserService.get_all(session, limit=None, offset=None)

            tasks = []
            for user in users_to_send:
                try:
                    task = asyncio.create_task(
                        _send_user_report(bot, user.id, report_text)
                    )
                    tasks.append(task)
                except Exception as e:
                    logger.error(
                        f"Ошибка создания задачи для пользователя {user.id}: {e}"
                    )

            await asyncio.gather(*tasks, return_exceptions=True)

    return True


async def _send_user_report(
    bot: Bot, user_id: int, report_text: str, media: list
) -> None:
    try:
        message = await bot.send_message(chat_id=user_id, text=report_text)

        if media:
            await bot.send_media_group(
                chat_id=user_id, reply_to_message_id=message.message_id
            )
    except Exception as e:
        logger.error(f"Ошибка отправки отчета пользователю {user_id}: {e}")


async def get_short_statistics():
    pass
