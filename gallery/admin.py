from django.contrib import admin
from .models import Album, Media


class MediaInline(admin.TabularInline):
    model = Media
    extra = 0
    fields = ("media_type", "file", "video_url", "title", "is_public", "uploaded_by", "uploaded_at")
    readonly_fields = ("uploaded_at",)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "created_at")
    search_fields = ("title",)
    inlines = [MediaInline]


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("__str__", "album", "media_type", "uploaded_by", "is_public", "uploaded_at")
    list_filter = ("media_type", "is_public")
    search_fields = ("title",)
