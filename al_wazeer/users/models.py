"""Data Models for al_wazeer.users"""

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    """AlWazeer Users"""

    image = models.ImageField(
        null=True,
        blank=True,
        upload_to="images/users",
        help_text="Profile picture",
    )
    bio = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text="User bio",
    )

    @property
    def chat_count(self):
        """Number of chats of a user"""

        return self.chats.count()
