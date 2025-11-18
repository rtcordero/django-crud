from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from tasks.api import TaskViewSet

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, 'tasks')

urlpatterns = [
    # API endpoints
    path("api/v1/", include(router.urls)),

    # OpenAPI 3.0 Schema
    path('schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI (interactiva, moderna)
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # ReDoc (documentación alternativa, muy elegante)
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
