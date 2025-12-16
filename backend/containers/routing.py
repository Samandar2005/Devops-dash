from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/containers/(?P<container_id>[^/]+)/logs/$', consumers.LogConsumer.as_asgi()),
    # Yangi qator:
    re_path(r'ws/containers/(?P<container_id>[^/]+)/stats/$', consumers.StatsConsumer.as_asgi()),
]