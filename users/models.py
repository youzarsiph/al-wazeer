""" Data Models for botland.users """

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    """BotLand Users"""

    image = models.ImageField(
        null=True,
        blank=True,
        upload_to="images/users",
        help_text="Profile picture",
    )
