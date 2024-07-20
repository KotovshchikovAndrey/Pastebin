from datetime import timedelta
from celery import Celery

import sys
import pathlib


APP_PATH = pathlib.Path(".").joinpath("..", "..")
sys.path.append(str(APP_PATH.absolute()))

from config import settings


celery = Celery(
    __name__,
    broker=settings.background.broker_url,
    backend=settings.background.broker_url,
    include=["tasks"],
)

celery.conf.update(
    enable_utc=True,
    timezone="UTC",
    beat_schedule={
        "cache-popular-pastes-every-day": {
            "task": "tasks.cache_popular_pastes",
            "schedule": timedelta(days=1),
        },
        "delete-expired-pastes-every-week": {
            "task": "tasks.delete_expired_pastes",
            "schedule": timedelta(weeks=1),
        },
    },
)
