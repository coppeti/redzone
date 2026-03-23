from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("gallery/", views.gallery, name="gallery"),
    path("gallery/<int:pk>/", views.gallery_album, name="gallery-album"),
]
