from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('braille-reader/', include('braille_reader.urls')),
    path('admin/', admin.site.urls),
]
