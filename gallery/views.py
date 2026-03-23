import io
import re
import uuid

from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404, redirect, render
from PIL import Image

from .forms import AlbumForm, PhotoUploadForm, VideoUploadForm
from .models import Album, Media

MAX_IMAGE_DIMENSION = 1920
JPEG_QUALITY = 85
MAX_PHOTO_MB = 10
VIDEO_RE = re.compile(
    r'(youtube\.com/watch\?.*v=|youtu\.be/)[a-zA-Z0-9_-]{11}'
    r'|vimeo\.com/\d+'
    r'|odysee\.com'
)


def _process_image(uploaded_file):
    img = Image.open(uploaded_file)
    if img.mode != "RGB":
        img = img.convert("RGB")
    if img.width > MAX_IMAGE_DIMENSION or img.height > MAX_IMAGE_DIMENSION:
        img.thumbnail((MAX_IMAGE_DIMENSION, MAX_IMAGE_DIMENSION), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=JPEG_QUALITY, optimize=True)
    buf.seek(0)
    return ContentFile(buf.read())


def _get_or_create_album(request):
    """Returns (album, error_message)."""
    album_id = request.POST.get("album", "").strip()
    new_name = request.POST.get("new_album_name", "").strip()
    if album_id:
        return get_object_or_404(Album, pk=album_id), None
    if new_name:
        return Album.objects.create(title=new_name, created_by=request.user), None
    return None, "Choisis une galerie ou saisis le nom d'une nouvelle galerie."


@login_required
def upload(request):
    albums = Album.objects.all()
    errors = []

    if request.method == "POST":
        media_type = request.POST.get("media_type", "photo")
        album, err = _get_or_create_album(request)
        if err:
            errors.append(err)
        else:
            if media_type == Media.PHOTO:
                files = request.FILES.getlist("file")
                if not files:
                    errors.append("Sélectionne au moins une photo.")
                else:
                    for i, f in enumerate(files):
                        if request.POST.get(f"removed_{i}") == "1":
                            continue
                        name = f.name.lower()
                        if not (name.endswith(".jpg") or name.endswith(".jpeg")):
                            errors.append(f"« {f.name} » n'est pas un fichier JPG.")
                            continue
                        if f.size > MAX_PHOTO_MB * 1024 * 1024:
                            errors.append(f"« {f.name} » dépasse {MAX_PHOTO_MB} Mo.")
                            continue
                        media = Media(
                            album=album,
                            uploaded_by=request.user,
                            media_type=Media.PHOTO,
                            title=request.POST.get(f"title_{i}", ""),
                            is_public=f"is_public_{i}" in request.POST,
                        )
                        processed = _process_image(f)
                        media.file.save(f"{uuid.uuid4().hex}.jpg", processed, save=False)
                        media.save()
                    if not errors:
                        return redirect("member-space")

            elif media_type == Media.VIDEO:
                video_url = request.POST.get("video_url", "").strip()
                if not video_url:
                    errors.append("Entre une URL YouTube.")
                elif not VIDEO_RE.search(video_url):
                    errors.append("Seules les URLs YouTube, Vimeo et Odysee sont acceptées.")
                else:
                    Media.objects.create(
                        album=album,
                        uploaded_by=request.user,
                        media_type=Media.VIDEO,
                        video_url=video_url,
                        title=request.POST.get("title", ""),
                        is_public="is_public" in request.POST,
                    )
                    return redirect("member-space")

    return render(request, "gallery/upload.html", {
        "albums": albums,
        "has_albums": albums.exists(),
        "errors": errors,
    })


@login_required
def album_list(request):
    albums = Album.objects.all().prefetch_related("medias")
    return render(request, "gallery/album_list.html", {"albums": albums})


@login_required
def album_create(request):
    if request.method == "POST":
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.created_by = request.user
            album.save()
            return redirect("album-detail", pk=album.pk)
    else:
        form = AlbumForm()
    return render(request, "gallery/album_create.html", {"form": form})


@login_required
def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk)
    photos = album.medias.filter(media_type=Media.PHOTO)
    videos = album.medias.filter(media_type=Media.VIDEO)
    return render(request, "gallery/album_detail.html", {
        "album": album,
        "photos": photos,
        "videos": videos,
    })


@login_required
def media_upload(request, pk):
    album = get_object_or_404(Album, pk=pk)
    video_form = VideoUploadForm(prefix="video")
    errors = []

    if request.method == "POST":
        media_type = request.POST.get("media_type")
        if media_type == Media.PHOTO:
            files = request.FILES.getlist("file")
            if not files:
                errors.append("Sélectionne au moins une photo.")
            else:
                for i, f in enumerate(files):
                    if request.POST.get(f"removed_{i}") == "1":
                        continue
                    name = f.name.lower()
                    if not (name.endswith(".jpg") or name.endswith(".jpeg")):
                        errors.append(f"« {f.name} » n'est pas un fichier JPG.")
                        continue
                    if f.size > MAX_PHOTO_MB * 1024 * 1024:
                        errors.append(f"« {f.name} » dépasse {MAX_PHOTO_MB} Mo.")
                        continue
                    media = Media(
                        album=album,
                        uploaded_by=request.user,
                        media_type=Media.PHOTO,
                        title=request.POST.get(f"title_{i}", ""),
                        is_public=f"is_public_{i}" in request.POST,
                    )
                    processed = _process_image(f)
                    media.file.save(f"{uuid.uuid4().hex}.jpg", processed, save=False)
                    media.save()
                if not errors:
                    return redirect("album-detail", pk=album.pk)
        elif media_type == Media.VIDEO:
            video_form = VideoUploadForm(request.POST, prefix="video")
            if video_form.is_valid():
                media = video_form.save(commit=False)
                media.album = album
                media.uploaded_by = request.user
                media.media_type = Media.VIDEO
                media.save()
                return redirect("album-detail", pk=album.pk)

    return render(request, "gallery/media_upload.html", {
        "album": album,
        "video_form": video_form,
        "errors": errors,
    })


@login_required
def media_delete(request, pk, media_pk):
    album = get_object_or_404(Album, pk=pk)
    media = get_object_or_404(Media, pk=media_pk, album=album)
    if request.method == "POST":
        if media.file:
            media.file.delete(save=False)
        media.delete()
    return redirect("album-detail", pk=album.pk)
