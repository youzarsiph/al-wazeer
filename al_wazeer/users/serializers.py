""" Serializers for al_wazeer.users """

from rest_framework.serializers import ModelSerializer
from al_wazeer.users.models import User


# Create your serializers here.
class UserSerializer(ModelSerializer):
    """Serialize users"""

    class Meta:
        """Meta data"""

        model = User
        fields = (
            "id",
            "url",
            "image",
            "username",
            "email",
            "first_name",
            "last_name",
            "chat_count",
        )
