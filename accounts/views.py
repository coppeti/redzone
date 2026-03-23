from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from gallery.models import Album


@login_required
def member_space(request):
    albums = Album.objects.all()
    return render(request, "redzone/member_space.html", {"albums": albums})


@login_required
def profile(request):
    return render(request, "redzone/profile.html")
