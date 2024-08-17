""" Views for botland.chats """

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from botland.chats.models import Chat
from botland.chats.serializers import ChatRetrieveSerializer, ChatSerializer
from botland.mixins import OwnerMixin


# Create your views here.
class ChatViewSet(OwnerMixin, ModelViewSet):
    """Chat ViewSet"""

    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ("id", "user", "bot")
    search_fields = ("user", "bot", "title")
    ordering_fields = ("id", "title", "created_at", "updated_at")

    def get_serializer_class(self):
        if self.action == "retrieve":
            self.serializer_class = ChatRetrieveSerializer

        return super().get_serializer_class()
