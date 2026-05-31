from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('app1.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ↑ This line makes Django serve uploaded files in development (DEBUG=True).
# In production, your web server (Nginx/Apache) should serve MEDIA_ROOT directly.