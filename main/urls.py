from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("gallery/", views.gallery, name="gallery"),
    path("red-zone/", views.redzone, name="red_zone"),
]
