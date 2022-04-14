import os

import celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = celery.Celery('shop')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
