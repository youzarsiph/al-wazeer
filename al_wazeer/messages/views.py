""" Views for al_wazeer.messages """

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from al_wazeer.messages.models import Message
from al_wazeer.messages.serializers import MessageCreateSerializer, MessageSerializer
from al_wazeer.mixins import OwnerMixin
from al_wazeer.permissions import IsOwner


# Create your views here.
class MessageViewSet(OwnerMixin, ModelViewSet):
    """Create, read, update and delete Messages"""

    queryset = Message.objects.prefetch_related("assistant", "chat")
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    search_fields = ("assistant", "chat", "content")
    ordering_fields = ("id", "created_at", "updated_at")
    filterset_fields = ("id", "assistant", "chat", "is_starred", "is_read")

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.serializer_class = MessageCreateSerializer

        return super().get_serializer_class()
