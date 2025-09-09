from django.contrib.auth import views as auth_views
from django.urls import path

from .forms import CustomAuthenticationForm

from . import views

urlpatterns = [
    path(
        "redzone/",
        auth_views.LoginView.as_view(
            template_name="redzone/login.html",
            authentication_form=CustomAuthenticationForm,
        ),
        name="redzone",
    ),
    path("membres/", views.member_space, name="member-space"),
]
