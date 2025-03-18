"""Serializers for al_wazeer.chats"""

from rest_framework.serializers import ModelSerializer

from al_wazeer.chats.models import Chat


# Create your serializers here.
class ChatSerializer(ModelSerializer):
    """Serialize chats"""

    class Meta:
        """Meta data"""

        model = Chat
        fields = (
            "id",
            "url",
            "assistant",
            "title",
            "description",
            "role",
            "is_pinned",
            "message_count",
            "created_at",
            "updated_at",
        )
