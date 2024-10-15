""" Serializers for botland.messages """

from rest_framework.serializers import ModelSerializer
from botland.messages.models import Message


# Create your serializers here.
class MessageCreateSerializer(ModelSerializer):
    """Serialize messages for create action"""

    class Meta:
        """Meta data"""

        model = Message
        read_only_fields = ("bot", "chat")
        fields = (
            "id",
            "url",
            "bot",
            "chat",
            "content",
            "is_read",
            "is_starred",
            "is_edited",
            "created_at",
            "updated_at",
        )


class MessageSerializer(MessageCreateSerializer):
    """Serialize messages"""

    class Meta(MessageCreateSerializer.Meta):
        """Meta data"""

        depth = 1
