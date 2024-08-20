""" Serializers for botland.chats """

from rest_framework.serializers import ModelSerializer
from botland.chats.models import Chat
from botland.messages.serializers import MessageSerializer
from botland.users.serializers import UserSerializer


# Create your serializers here.
class ChatCreateSerializer(ModelSerializer):
    """Serialize chats for create action"""

    class Meta:
        """Meta data"""

        model = Chat
        read_only_fields = ("bot",)
        fields = (
            "id",
            "url",
            "bot",
            "title",
            "is_pinned",
            "message_count",
            "unread_message_count",
            "created_at",
            "updated_at",
        )


class ChatSerializer(ModelSerializer):
    """Serialize chats"""

    user = UserSerializer()

    class Meta:
        """Meta data"""

        depth = 1
        model = Chat
        read_only_fields = ("user", "bot")
        fields = (
            "id",
            "url",
            "user",
            "bot",
            "title",
            "is_pinned",
            "message_count",
            "unread_message_count",
            "created_at",
            "updated_at",
        )


class ChatRetrieveSerializer(ChatSerializer):
    """Serialize chats in retrieve action"""

    messages = MessageSerializer(many=True)

    class Meta(ChatSerializer.Meta):
        """Meta data"""

        fields = (
            "id",
            "url",
            "bot",
            "title",
            "is_pinned",
            "message_count",
            "unread_message_count",
            "created_at",
            "updated_at",
            "messages",
        )
        read_only_fields = ChatSerializer.Meta.read_only_fields + ("messages",)
