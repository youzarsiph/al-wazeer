""" Serializers for botland.messages """

from rest_framework.serializers import ModelSerializer
from botland.messages.models import Message
from botland.users.serializers import UserSerializer


# Create your serializers here.
class MessageCreateSerializer(ModelSerializer):
    """Serialize messages for create action"""

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
            "is_read",
            "is_starred",
            "is_edited",
            "created_at",
            "updated_at",
        )


class MessageSerializer(ModelSerializer):
    """Serialize messages"""

    user = UserSerializer()

    class Meta:
        """Meta data"""

        depth = 1
        model = Message
        read_only_fields = ("user", "bot", "chat")
        fields = (
            "id",
            "url",
            "user",
            "bot",
            "chat",
            "content",
            "is_read",
            "is_starred",
            "is_edited",
            "created_at",
            "updated_at",
        )
