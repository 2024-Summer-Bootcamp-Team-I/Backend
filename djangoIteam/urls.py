from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
schema_view = get_schema_view(
    openapi.Info(
        title="Fakenews",
        default_version='1.0',
    ),
    public=True,
    permission_classes=[AllowAny],
    url='https://fakenew.site',
)
urlpatterns = [
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("admin/", admin.site.urls),
    path("api/v1/accounts/", include('accounts.urls')),
    path("api/v1/channels/", include('channels.urls')),
    path('api/v1/news/', include('news.urls')),
    path("api/v1/classifies/<int:news_id>/feedbacks/", include('feedbacks.urls')),
    path("api/v1/classifies/", include('classify_news.urls')),
    path("api/v1/scraps/", include('scraped_news.urls')),
    path('', include('django_prometheus.urls')),
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
# Ensure Django uses HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True