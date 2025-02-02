from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("read/", views.read, name="read"),
    path("image-to-braille/", views.image_to_braille, name="image_to_braille"),
    path("braille-to-english/", views.braille_to_english, name="braille_to_english"),
]