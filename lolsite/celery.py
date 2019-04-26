from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lolsite.settings')

app = Celery('lolsite', broker=settings.BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)

app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-champion-info-every-day': {
        'task': 'main.tasks.update_champion_info',
        'schedule': crontab(minute=0, hour=0),
        'args': (),
    },
}
