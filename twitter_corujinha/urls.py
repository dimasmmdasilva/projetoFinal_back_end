import os
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('twitter_corujinha.core.urls')),  # Inclui todas as rotas definidas no core.urls
]

if settings.DEBUG or 'RENDER_EXTERNAL_HOSTNAME' in os.environ:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

