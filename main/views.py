import os

from django.shortcuts import render
from django.conf import settings


def home(request):
    bikers_path = os.path.join(settings.BASE_DIR, "static", "img", "bikers")
    bikers_images = []

    if os.path.exists(bikers_path):
        for filename in os.listdir(bikers_path):
            if filename.endswith(".jpg"):
                bikers_images.append(f"img/bikers/{filename}")

    context = {"bikers_images": bikers_images}
    return render(request, "main/home.html", context)


def gallery(request):
    return render(request, "main/gallery.html")


def redzone(request):
    return render(request, "main/redzone.html")
