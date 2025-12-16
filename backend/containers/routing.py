from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # ESKI: r'ws/containers/(?P<container_id>\w+)/logs/$'
    # YANGI (Defis va boshqa belgilarni qabul qiladi):
    re_path(r'ws/containers/(?P<container_id>[^/]+)/logs/$', consumers.LogConsumer.as_asgi()),
]