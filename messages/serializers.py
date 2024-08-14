""" Serializers for botland.messages """

from rest_framework.serializers import ModelSerializer
from botland.messages.models import Message


# Create your serializers here.
class MessageSerializer(ModelSerializer):
    """Serialize messages"""

    class Meta:
        """Meta data"""

        model = Message
        fields = ()
        read_only_fields = ()
