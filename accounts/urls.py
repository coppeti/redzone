from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path(
        "redzone/",
        auth_views.LoginView.as_view(template_name="redzone/login.html"),
        name="redzone",
    )
]
