"""Data Models for al_wazeer.messages"""

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
        help_text="Message owner",
    )
    assistant = models.ForeignKey(
        "assistants.Assistant",
        on_delete=models.CASCADE,
        related_name="messages",
        null=True,
        blank=True,
        help_text="Message assistant",
    )
    chat = models.ForeignKey(
        "chats.Chat",
        on_delete=models.CASCADE,
        related_name="messages",
        null=True,
        blank=True,
        help_text="Message chat",
    )
    content = models.TextField(
        db_index=True,
        help_text="Message content",
    )
    is_starred = models.BooleanField(
        default=False,
        help_text="Designates if the message is added to starred messages",
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
        return (
            f"{self.assistant if self.assistant else self.user}: {self.content[:10]}..."
        )
