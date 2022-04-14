import os

import celery
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = celery.Celery('shop')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'mailing.tasks.send_mail_to_user_without_payment',
        'schedule': crontab(day_of_week='monday'),
    },
    'add-every-monday': {
        'task': 'mailing.tasks.send_mail_to_everyone',
        'schedule': crontab(day_of_week='monday'),
    },
}
