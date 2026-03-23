from django.db import models
from django.conf import settings


class Album(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="albums",
        verbose_name="Créé par",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")

    class Meta:
        verbose_name = "Album"
        verbose_name_plural = "Albums"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Media(models.Model):
    PHOTO = "photo"
    VIDEO = "video"
    TYPE_CHOICES = [(PHOTO, "Photo"), (VIDEO, "Vidéo")]

    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="medias",
        verbose_name="Album",
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="medias",
        verbose_name="Uploadé par",
    )
    media_type = models.CharField(
        max_length=5,
        choices=TYPE_CHOICES,
        verbose_name="Type",
    )
    file = models.ImageField(
        upload_to="gallery/photos/",
        blank=True,
        verbose_name="Fichier",
    )
    video_url = models.URLField(
        blank=True,
        verbose_name="URL vidéo (YouTube/Vimeo)",
    )
    title = models.CharField(max_length=200, blank=True, verbose_name="Titre")
    is_public = models.BooleanField(default=False, verbose_name="Public")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Uploadé le")

    class Meta:
        verbose_name = "Média"
        verbose_name_plural = "Médias"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title or f"{self.get_media_type_display()} — {self.album}"
