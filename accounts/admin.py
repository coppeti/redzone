from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "email",
        "firstname",
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
    ordering = ("email",)

    # Modification des champs pour l'administration
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Informations personnelles",
            {
                "fields": (
                    "firstname",
                    "nickname",
                    "aka1",
                    "aka2",
                    "aka3",
                    "aka4",
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
                    "email",
                    "password1",
                    "password2",
                    "firstname",
                    "nickname",
                    "aka1",
                    "aka2",
                    "aka3",
                    "aka4",
                    "picture",
                ),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
