from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def member_space(request):
    return render(request, "redzone/member_space.html")
