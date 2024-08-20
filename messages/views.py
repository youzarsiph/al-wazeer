""" Views for botland.messages """

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from botland.messages.models import Message
from botland.messages.serializers import MessageCreateSerializer, MessageSerializer
from botland.mixins import OwnerMixin
from botland.permissions import IsOwner


# Create your views here.
class MessageViewSet(OwnerMixin, ModelViewSet):
    """Message ViewSet"""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    search_fields = ("content",)
    ordering_fields = ("id", "created_at", "updated_at")
    filterset_fields = ("id", "user", "bot", "chat", "is_starred", "is_read")

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "delete"]:
            self.serializer_class = MessageCreateSerializer

        return super().get_serializer_class()
