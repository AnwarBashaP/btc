import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stocks.settings")
app = Celery("stocks")
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')
app.config_from_object(settings, namespace="CELERY")

app.conf.beat_schedule = {
    'price-alert-trigger': {
        'task': 'market.tasks.check_price_and_send_alerts',
        'schedule': 1,
    },
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
