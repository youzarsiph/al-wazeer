""" Views for botland.messages """

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from botland.messages.models import Message
from botland.messages.serializers import MessageSerializer
from botland.mixins import OwnerMixin


# Create your views here.
class MessageViewSet(OwnerMixin, ModelViewSet):
    """Message ViewSet"""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ("id", "user", "bot", "chat", "is_starred")
    search_fields = ("content",)
    ordering_fields = ("id", "created_at", "updated_at")


class ChatMessagesViewSet(MessageViewSet):
    """Messages of a chat"""

    def get_queryset(self):
        """Filter queryset by chat"""

        return super().get_queryset().filter(chat_id=self.kwargs["id"])

    def perform_create(self, serializer):
        """Saves the message with user and chat"""

        serializer.save(user=self.request.user, chat_id=self.kwargs["id"])
