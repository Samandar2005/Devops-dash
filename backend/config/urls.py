from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Swagger va JWT importlari
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Swagger konfiguratsiyasi
schema_view = get_schema_view(
   openapi.Info(
      title="DevOps Dashboard API",
      default_version='v1',
      description="API documentation for Mini-PaaS",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Tokenni yangilash
    
    # Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)