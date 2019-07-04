import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CMLMasterProject.settings')

app = Celery('CMLMasterProject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()