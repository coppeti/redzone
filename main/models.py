from django.db import models


class MemberCard(models.Model):
    name = models.CharField(max_length=100)
    aka1 = models.CharField(max_length=100, blank=True)
    aka2 = models.CharField(max_length=100, blank=True)
    aka3 = models.CharField(max_length=100, blank=True)
    aka4 = models.CharField(max_length=100, blank=True)
    picture = models.ImageField(blank=False, upload_to="members/")
