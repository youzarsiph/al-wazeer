""" Data Models for botland.chats """

from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()


class Chat(models.Model):
    """BotLand Chats"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chats",
        help_text="User",
    )
    bot = models.ForeignKey(
        "bots.Bot",
        on_delete=models.CASCADE,
        related_name="chats",
        help_text="Chatbot (Chat LLM)",
    )
    title = models.CharField(
        max_length=128,
        db_index=True,
        help_text="Chat title",
    )
    is_pinned = models.BooleanField(
        default=False,
        help_text="Designates if the chat is pinned",
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
    def message_count(self) -> int:
        """Number of a messages of a chat"""

        return self.messages.count()

    def __str__(self) -> str:
        return f"{self.user}-{self.bot}: {self.title}"
