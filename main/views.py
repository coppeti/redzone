from django.shortcuts import render

from accounts.models import CustomUser
from gallery.models import Media


def home(request):
    bikers = CustomUser.objects.filter(is_active=True).order_by("rank")
    return render(request, "main/home.html", {"bikers": bikers})


def gallery(request):
    from gallery.models import Album
    albums = Album.objects.filter(medias__is_public=True).distinct().order_by("-created_at")
    return render(request, "main/gallery.html", {"albums": albums})


def gallery_album(request, pk):
    from django.shortcuts import get_object_or_404
    from gallery.models import Album, Media
    album = get_object_or_404(Album, pk=pk)
    photos = album.medias.filter(is_public=True, media_type=Media.PHOTO)
    videos = album.medias.filter(is_public=True, media_type=Media.VIDEO)
    return render(request, "main/gallery_album.html", {
        "album": album,
        "photos": photos,
        "videos": videos,
    })
