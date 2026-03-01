from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/audio/", include("audio_core.urls")),
    path("api/audio_analysis/", include("audio_analysis.urls")),
    path("api/ghl_integration/", include("ghl_integration.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
