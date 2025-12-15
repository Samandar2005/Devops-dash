from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Masalan: ws://localhost:8000/ws/containers/123/logs/
    re_path(r'ws/containers/(?P<container_id>\w+)/logs/$', consumers.LogConsumer.as_view()),
]