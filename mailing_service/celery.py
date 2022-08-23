import os
from celery import Celery
from celery.schedules import crontab

from mailing_service import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailing_service.settings')

app = Celery("mailing_service")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'run-mailings-every-1-minute': {
        'task': 'mailing.tasks.run_mailings',
        'schedule': crontab(minute='*/1'),

    },
}
app.conf.timezone = 'UTC'
