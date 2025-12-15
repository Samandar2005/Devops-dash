import os
from celery import Celery

# Djangoning settings faylini standart sifatida belgilash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Barcha sozlamalarni settings.py dan oladi (CELERY_ bilan boshlanadiganlarini)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Har bir app ichidan tasks.py faylini qidiradi
app.autodiscover_tasks()