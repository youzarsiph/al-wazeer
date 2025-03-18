"""Data Models for al_wazeer.chats"""

from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()


class Chat(models.Model):
    """Chats"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chats",
        help_text="Chat owner",
    )
    assistant = models.ForeignKey(
        "assistants.Assistant",
        on_delete=models.CASCADE,
        related_name="chats",
        help_text="Chat assistant",
    )
    title = models.CharField(
        max_length=128,
        db_index=True,
        help_text="Chat title",
    )
    description = models.CharField(
        max_length=512,
        db_index=True,
        help_text="Chat description",
    )
    role = models.CharField(
        max_length=1024,
        default="You are a helpful assistant.",
        help_text="The role that the assistant will play.",
    )
    is_pinned = models.BooleanField(
        default=False,
        help_text="Designates if the chat is pinned",
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
    def message_count(self) -> int:
        """Number of messages"""

        return self.messages.count()

    def __str__(self) -> str:
        return f"{self.user}-{self.assistant}: {self.title}"
