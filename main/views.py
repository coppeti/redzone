import os

from django.shortcuts import render
from django.conf import settings

from accounts.models import CustomUser


def home(request):
    bikers = CustomUser.objects.filter(is_active=True).order_by("rank")
    context = {
        "bikers": bikers,
    }
    return render(request, "main/home.html", context)


def gallery(request):
    return render(request, "main/gallery.html")
