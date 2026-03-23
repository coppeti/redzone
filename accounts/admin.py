from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import PasswordResetForm

from .models import CustomUser


@admin.action(description="Envoyer lien d'accès par email")
def send_access_email(modeladmin, request, queryset):
    for user in queryset:
        form = PasswordResetForm({"email": user.email})
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name="registration/password_reset_email.html",
                subject_template_name="registration/password_reset_subject.txt",
            )
    modeladmin.message_user(request, f"Email(s) envoyé(s) à {queryset.count()} membre(s).")


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    actions = [send_access_email]
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
