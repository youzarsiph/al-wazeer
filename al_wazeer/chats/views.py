""" Views for al_wazeer.chats """

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from al_wazeer.chats.models import Chat
from al_wazeer.chats.serializers import (
    ChatCreateSerializer,
    ChatRetrieveSerializer,
    ChatSerializer,
)
from al_wazeer.mixins import OwnerMixin
from al_wazeer.permissions import IsOwner


# Create your views here.
class ChatViewSet(OwnerMixin, ModelViewSet):
    """Create, read, update and delete chats"""

    queryset = Chat.objects.prefetch_related("assistant", "messages")
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    filterset_fields = ("id", "user", "assistant")
    search_fields = ("title", "messages__content")
    ordering_fields = ("id", "title", "created_at", "updated_at")

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = ChatCreateSerializer
        elif self.action == "retrieve":
            self.serializer_class = ChatRetrieveSerializer

        return super().get_serializer_class()
