from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    avatar = models.ImageField(
        upload_to="users/avatars/%Y/%m/%d/", default="users/avatars/default.jpg"
    )
    bio = models.TextField(max_length=500, null=True)
    location = models.CharField(max_length=30, null=True)
    website = models.CharField(max_length=100, null=True)
    joined_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "users"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
