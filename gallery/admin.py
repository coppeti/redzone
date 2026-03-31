from django.contrib import admin
from .models import Album, Media


def file_size(obj):
    if obj.file:
        size = obj.file.size
        if size >= 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} Mo"
        return f"{size / 1024:.0f} Ko"
    return "—"

file_size.short_description = "Taille"


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
    list_display = ("__str__", "album", "media_type", "uploaded_by", "is_public", file_size, "uploaded_at")
    list_filter = ("album", "media_type", "is_public")
    search_fields = ("title",)
