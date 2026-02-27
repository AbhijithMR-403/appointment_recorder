import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize# the configuration object to child processes
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'make-api-call': {
        'task': 'ghl_integration.tasks.make_refresh_token_call',
        'schedule': 240.0, # 4 minutes
        # 'schedule': 36000.0, # 10 hours
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')