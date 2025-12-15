from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # XATO: consumers.LogConsumer.as_view()
    # TO'G'RI: consumers.LogConsumer.as_asgi()
    re_path(r'ws/containers/(?P<container_id>\w+)/logs/$', consumers.LogConsumer.as_asgi()),
]