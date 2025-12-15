import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Django ishga tushishi kerak (modellar yuklanishi uchun)
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import containers.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app, # Oddiy API so'rovlar
    "websocket": AuthMiddlewareStack(
        URLRouter(
            containers.routing.websocket_urlpatterns
        )
    ),
})