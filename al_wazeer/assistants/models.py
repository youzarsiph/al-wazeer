"""Data Models for al_wazeer.assistants"""

from django.db import models


# Create your models here.
class Assistant(models.Model):
    """Al-Wuzaraa AI assistants"""

    image = models.ImageField(
        upload_to="images/assistants/",
        help_text="Assistant image",
    )
    name = models.CharField(
        max_length=128,
        unique=True,
        db_index=True,
        help_text="Assistant name",
    )
    model = models.CharField(
        max_length=128,
        unique=True,
        db_index=True,
        help_text="Can be a model id hosted on the Hugging Face Hub, "
        "e.g. `meta-llama/Meta-Llama-3-8B-Instruct` or a URL to a deployed Inference Endpoint.",
    )
    description = models.CharField(
        max_length=512,
        help_text="Assistant description",
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
    def chat_count(self) -> int:
        """Number of chats of an assistant"""

        return self.chats.count()

    @property
    def model_url(self) -> str:
        """URL of the model (LLM) on HuggingFace Hub"""

        return f"https://huggingface.co/{self.model}"

    def __str__(self) -> str:
        return self.name
