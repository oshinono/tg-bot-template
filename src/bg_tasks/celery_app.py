from celery import Celery
from database import REDIS_URL
from bg_tasks.consts import INIT_SCHEDULE_TIME
from consts import CURRENT_TIMEZONE
import pytz
from redbeat import RedBeatSchedulerEntry
from celery.schedules import crontab
from datetime import datetime
from loguru import logger
from utils import setup_logger

app = Celery("bg_tasks")

app.conf.broker_url = REDIS_URL
app.conf.result_backend = REDIS_URL
app.conf.timezone = CURRENT_TIMEZONE

app.conf.beat_schedule = {
    "scan": {
        "task": "bg_tasks.celery_task.celery_task",
        "schedule": INIT_SCHEDULE_TIME,
    },
}


def update_schedule(task_name: str, new_schedule: crontab) -> bool:
    task = "bg_tasks.celery_task.celery_task"
    try:
        if not hasattr(new_schedule, "nowfun"):
            new_schedule.nowfun = lambda: datetime.now(pytz.timezone(CURRENT_TIMEZONE))

        entry = RedBeatSchedulerEntry(
            name=task_name, task=task, schedule=new_schedule, app=app
        )
        entry.save()
        return True
    except Exception as e:
        logger.error(f"Ошибка при обновлении расписания: {str(e)}")
        return False


# update_schedule('scan-posts', crontab(hour=21, minute=38)) # W, оно работает, мск формат
setup_logger("celery")
