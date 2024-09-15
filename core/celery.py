import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('voting_system', broker=settings.BROKER_URL)



app.conf.broker_url = settings.BROKER_URL
app.conf.redbeat_redis_url = settings.BROKER_URL + "/1"
app.conf.result_backend = settings.BROKER_URL + '/0'
app.conf.redbeat_lock_key = None

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.update(
    result_backend=settings.CELERY_RESULT_BACKEND,
)