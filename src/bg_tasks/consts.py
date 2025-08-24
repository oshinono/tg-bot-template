from celery.schedules import crontab

INIT_SCHEDULE_TIME = crontab(hour=10, minute=0)
