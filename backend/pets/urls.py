from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from pets.apps.main.views import error404


handler404 = error404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('pets.apps.api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



