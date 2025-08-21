from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _


# Manager personnalisé pour CustomUser
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Crée un utilisateur avec un email et un mot de passe.
        """
        if not email:
            raise ValueError(_("L'adresse email est requise"))
        email = self.normalize_email(email)  # Normalisation (minuscule etc.)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crée un super utilisateur (admin).
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


# Modèle utilisateur personnalisé
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Adresse email")
    rank = models.IntegerField(max_length=2, default=99, verbose_name="Rang")
    firstname = models.CharField(
        max_length=30, blank=True, verbose_name="Prénom"
    )
    nickname = models.CharField(
        max_length=100, blank=True, verbose_name="Surnom"
    )  # Equivalent au champ `name` de UserProfile
    aka1 = models.CharField(max_length=100, blank=True, verbose_name="Alias 1")
    aka2 = models.CharField(max_length=100, blank=True, verbose_name="Alias 2")
    aka3 = models.CharField(max_length=100, blank=True, verbose_name="Alias 3")
    aka4 = models.CharField(max_length=100, blank=True, verbose_name="Alias 4")
    description = models.TextField(blank=True, verbose_name="Présentation")
    picture = models.ImageField(
        upload_to="members/", blank=True, verbose_name="Photo"
    )  # Champ pour stocker la photo

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # Email utilisé comme identifiant unique
    REQUIRED_FIELDS = [
        "firstname",
        "nickname",
    ]  # Champs obligatoires pour la création d'utilisateur

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return self.firstname
