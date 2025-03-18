"""Serializers for al_wazeer.assistants"""

from rest_framework.serializers import ModelSerializer

from al_wazeer.assistants.models import Assistant


# Create your serializers here.
class AssistantSerializer(ModelSerializer):
    """Serialize Assistants"""

    class Meta:
        """Meta data"""

        model = Assistant
        fields = (
            "id",
            "url",
            "image",
            "name",
            "model",
            "model_url",
            "description",
            "chat_count",
            "created_at",
            "updated_at",
        )
