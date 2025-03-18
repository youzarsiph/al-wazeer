"""Serializers for al_wazeer.messages"""

from rest_framework.serializers import ModelSerializer

from al_wazeer.messages.models import Message


# Create your serializers here.
class MessageSerializer(ModelSerializer):
    """Serialize messages"""

    class Meta:
        """Meta data"""

        model = Message
        read_only_fields = ("chat", "assistant")
        fields = (
            "id",
            "chat",
            "assistant",
            "content",
            "is_starred",
            "is_edited",
            "created_at",
            "updated_at",
        )


class HyperLinkedMessageSerializer(MessageSerializer):
    """Serialize messages"""

    class Meta(MessageSerializer.Meta):
        """Meta data"""

        fields = (
            MessageSerializer.Meta.fields[:1]
            + ("url",)
            + MessageSerializer.Meta.fields[1:]
        )
