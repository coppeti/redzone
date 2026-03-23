import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Album, Media

MAX_PHOTO_SIZE_MB = 10


class UploadForm(forms.Form):
    # Gallery
    album = forms.ModelChoiceField(
        queryset=Album.objects.none(),
        required=False,
        empty_label="-- Choisir une galerie existante --",
        widget=forms.Select(attrs={"class": "input-redzone"}),
    )
    new_album_name = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"class": "input-redzone", "placeholder": "Nom de la nouvelle galerie"}),
    )

    # Media type
    media_type = forms.ChoiceField(
        choices=[(Media.PHOTO, "Photo"), (Media.VIDEO, "Vidéo")],
        initial=Media.PHOTO,
        widget=forms.RadioSelect(attrs={"class": "radio-type"}),
    )

    # Photo
    file = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"class": "input-file", "accept": ".jpg,.jpeg"}),
    )

    # Video
    video_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={"class": "input-redzone", "placeholder": "https://www.youtube.com/watch?v=..."}),
    )

    # Common
    title = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"class": "input-redzone", "placeholder": "Titre (optionnel)"}),
    )
    is_public = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "input-checkbox"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["album"].queryset = Album.objects.all()

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if file:
            name = file.name.lower()
            if not (name.endswith(".jpg") or name.endswith(".jpeg")):
                raise ValidationError("Seuls les fichiers JPG sont acceptés.")
            if file.size > MAX_PHOTO_SIZE_MB * 1024 * 1024:
                raise ValidationError(f"La photo ne doit pas dépasser {MAX_PHOTO_SIZE_MB} Mo.")
        return file

    def clean_video_url(self):
        url = self.cleaned_data.get("video_url")
        if url:
            pattern = r'(youtube\.com/watch\?.*v=|youtu\.be/)[a-zA-Z0-9_-]{11}'
            if not re.search(pattern, url):
                raise ValidationError("Seules les URLs YouTube sont acceptées (youtube.com ou youtu.be).")
        return url

    def clean(self):
        cleaned_data = super().clean()
        album = cleaned_data.get("album")
        new_album_name = cleaned_data.get("new_album_name")
        media_type = cleaned_data.get("media_type")
        file = cleaned_data.get("file")
        video_url = cleaned_data.get("video_url")

        if not album and not new_album_name:
            raise ValidationError("Choisis une galerie existante ou saisis le nom d'une nouvelle galerie.")

        if media_type == Media.PHOTO and not file:
            raise ValidationError("Sélectionne une photo JPG.")

        if media_type == Media.VIDEO and not video_url:
            raise ValidationError("Entre une URL YouTube.")

        return cleaned_data


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "input-redzone", "placeholder": "Titre de l'album"}),
            "description": forms.Textarea(attrs={"class": "input-redzone", "rows": 3, "placeholder": "Description (optionnel)"}),
        }


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ["file", "title", "is_public"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "input-redzone", "placeholder": "Titre (optionnel)"}),
            "is_public": forms.CheckboxInput(attrs={"class": "input-checkbox"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].required = True
        self.fields["file"].widget.attrs.update({"class": "input-file", "accept": "image/*"})


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ["video_url", "title", "is_public"]
        widgets = {
            "video_url": forms.URLInput(attrs={"class": "input-redzone", "placeholder": "https://youtube.com/watch?v=..."}),
            "title": forms.TextInput(attrs={"class": "input-redzone", "placeholder": "Titre (optionnel)"}),
            "is_public": forms.CheckboxInput(attrs={"class": "input-checkbox"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["video_url"].required = True
