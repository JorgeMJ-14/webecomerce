# ecommerce/urls.py
from django.contrib import admin
from django.urls import path, include  # Asegúrate de incluir include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),  # Incluye las URLs de la aplicación store
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
