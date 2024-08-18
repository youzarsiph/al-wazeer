""" Serializers for botland.chats """

from rest_framework.serializers import ModelSerializer
from botland.chats.models import Chat


# Create your serializers here.
class ChatSerializer(ModelSerializer):
    """Serialize chats"""

    class Meta:
        """Meta data"""

        model = Chat
        read_only_fields = ("user",)
        fields = (
            "id",
            "url",
            "user",
            "bot",
            "title",
            "is_pinned",
            "message_count",
            "created_at",
            "updated_at",
        )


class ChatRetrieveSerializer(ChatSerializer):
    """Serialize chats in retrieve action"""

    class Meta(ChatSerializer.Meta):
        """Meta data"""

        read_only_fields = ("user", "bot")
