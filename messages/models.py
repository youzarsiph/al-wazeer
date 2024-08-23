""" Data Models for botland.messages """

from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()


class Message(models.Model):
    """BotLand Messages"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages",
        null=True,
        blank=True,
        help_text="User",
    )
    bot = models.ForeignKey(
        "bots.Bot",
        on_delete=models.CASCADE,
        related_name="messages",
        null=True,
        blank=True,
        help_text="Bot",
    )
    chat = models.ForeignKey(
        "chats.Chat",
        on_delete=models.CASCADE,
        related_name="messages",
        help_text="Chat",
    )
    content = models.TextField(
        db_index=True,
        help_text="Message content",
    )
    is_read = models.BooleanField(
        default=False,
        help_text="Designates if the message is read or viewed by user",
    )
    is_starred = models.BooleanField(
        default=False,
        help_text="Designates if the message is saved or added to favorites",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Creation date and time",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last update date and time",
    )

    @property
    def is_edited(self) -> bool:
        """Designates if the message is edited"""

        return self.created_at != self.updated_at

    def __str__(self) -> str:
        return f"{self.user if self.user is not None else self.bot}: {self.content[:10]}..."
