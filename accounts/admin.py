from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "firstname",
        "email",
        "rank",
        "nickname",
        "aka1",
        "aka2",
        "aka3",
        "aka4",
        "picture",
        "is_staff",
        "is_superuser",
    )
    search_fields = ("email", "firstname", "nickname")
    ordering = ("firstname",)

    # Modification des champs pour l'administration
    fieldsets = (
        (None, {"fields": ("firstname", "password")}),
        (
            "Informations personnelles",
            {
                "fields": (
                    "email",
                    "rank",
                    "nickname",
                    "aka1",
                    "aka2",
                    "aka3",
                    "aka4",
                    "description",
                    "picture",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "firstname",
                    "email",
                    "password1",
                    "password2",
                    "rank",
                    "nickname",
                    "aka1",
                    "aka2",
                    "aka3",
                    "aka4",
                    "description",
                    "picture",
                ),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
