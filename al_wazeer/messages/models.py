""" Data Models for al_wazeer.messages """

from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()


class Message(models.Model):
    """AlWazeer Messages"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages",
        null=True,
        blank=True,
        help_text="User",
    )
    assistant = models.ForeignKey(
        "assistants.Assistant",
        on_delete=models.CASCADE,
        related_name="messages",
        null=True,
        blank=True,
        help_text="Assistant",
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
        help_text="Designates if the message is viewed by user",
    )
    is_starred = models.BooleanField(
        default=False,
        help_text="Designates if the message is saved or added to favorites",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date created",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last update",
    )

    @property
    def is_edited(self) -> bool:
        """Designates if the message is edited"""

        return self.created_at != self.updated_at

    def __str__(self) -> str:
        return f"{self.user if self.user is not None else self.assistant}: {self.content[:10]}..."
