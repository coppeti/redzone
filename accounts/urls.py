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
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path("membres/", views.member_space, name="member-space"),
    path("membres/profil/", views.profile, name="profile"),
    path(
        "membres/profil/mot-de-passe/",
        auth_views.PasswordChangeView.as_view(
            template_name="redzone/password_change.html",
            success_url="/membres/profil/mot-de-passe/ok/",
        ),
        name="password-change",
    ),
    path(
        "membres/profil/mot-de-passe/ok/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="redzone/password_change_done.html",
        ),
        name="password-change-done",
    ),
]
