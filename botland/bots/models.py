""" Data Models for botland.bots """

from django.db import models


# Create your models here.
class Bot(models.Model):
    """BotLand Bots"""

    name = models.CharField(
        max_length=128,
        db_index=True,
        help_text="Bot name (Chat LLM)",
    )
    model = models.CharField(
        max_length=128,
        unique=True,
        db_index=True,
        help_text="Can be a model id hosted on the Hugging Face Hub, e.g. `meta-llama/Meta-Llama-3-8B-Instruct` or a URL to a deployed Inference Endpoint.",
    )
    description = models.CharField(
        max_length=512,
        help_text="Bot description",
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
    def chat_count(self):
        """Number of chats of a bot"""

        return self.chats.count()

    def __str__(self) -> str:
        return self.name
