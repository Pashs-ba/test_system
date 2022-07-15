from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_sys.settings')

app = Celery("test_sys")
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()