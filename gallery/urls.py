from django.urls import path
from . import views

urlpatterns = [
    path("membres/upload/", views.upload, name="upload"),
    path("membres/galeries/", views.album_list, name="album-list"),
    path("membres/galeries/creer/", views.album_create, name="album-create"),
    path("membres/galeries/<int:pk>/", views.album_detail, name="album-detail"),
    path("membres/galeries/<int:pk>/upload/", views.media_upload, name="media-upload"),
    path("membres/galeries/<int:pk>/media/<int:media_pk>/supprimer/", views.media_delete, name="media-delete"),
]
