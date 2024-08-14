""" Serializers for botland.chats """

from rest_framework.serializers import ModelSerializer
from botland.chats.models import Chat


# Create your serializers here.
class ChatSerializer(ModelSerializer):
    """Serialize chats"""

    class Meta:
        """Meta data"""

        model = Chat
        fields = ()
        read_only_fields = ()
