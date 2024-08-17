""" Serializers for botland.messages """

from rest_framework.serializers import ModelSerializer
from botland.messages.models import Message


# Create your serializers here.
class MessageSerializer(ModelSerializer):
    """Serialize messages"""

    class Meta:
        """Meta data"""

        model = Message
        read_only_fields = ("user", "bot", "chat")
        fields = (
            "id",
            "url",
            "user",
            "bot",
            "chat",
            "content",
            "is_starred",
            "is_edited",
            "created_at",
            "updated_at",
        )
