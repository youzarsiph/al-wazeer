"""Views for al_wazeer.chats"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from al_wazeer.chats.models import Chat
from al_wazeer.chats.serializers import ChatSerializer
from al_wazeer.mixins import OwnerMixin
from al_wazeer.permissions import IsOwner


# Create your views here.
class ChatViewSet(OwnerMixin, ModelViewSet):
    """Create, read, update and delete chats"""

    queryset = Chat.objects.prefetch_related("assistant")
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    filterset_fields = ("id", "assistant")
    search_fields = ("title", "description", "role")
    ordering_fields = ("title", "created_at", "updated_at")
