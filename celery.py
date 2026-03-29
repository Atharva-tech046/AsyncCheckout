import os
from celery import Celery

# 1. Tell Celery where to find the Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# 2. Use a 'CELERY_' prefix for all configuration keys
app.config_from_object('django.conf:settings', namespace='CELERY')

# 3. Look for a 'tasks.py' file in every app (like checkout_logic)
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')