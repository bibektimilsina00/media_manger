from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from media.views import handle_media

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', handle_media, name='media_manager'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
