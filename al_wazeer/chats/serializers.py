""" Serializers for al_wazeer.chats """

from rest_framework.serializers import ModelSerializer

from al_wazeer.chats.models import Chat


# Create your serializers here.
class ChatCreateSerializer(ModelSerializer):
    """Serialize chats for create action"""

    class Meta:
        """Meta data"""

        model = Chat
        fields = (
            "id",
            "url",
            "assistant",
            "title",
            "is_pinned",
            "message_count",
            "unread_message_count",
            "created_at",
            "updated_at",
        )


class ChatSerializer(ChatCreateSerializer):
    """Serialize chats"""

    class Meta(ChatCreateSerializer.Meta):
        """Meta data"""

        depth = 1
        read_only_fields = ("assistant",)


class ChatRetrieveSerializer(ChatSerializer):
    """Serialize chats in retrieve action"""

    class Meta(ChatSerializer.Meta):
        """Meta data"""

        fields = ChatSerializer.Meta.fields + ("messages",)
        read_only_fields = ChatSerializer.Meta.read_only_fields + ("messages",)
