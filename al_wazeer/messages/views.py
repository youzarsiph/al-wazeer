"""Views for al_wazeer.messages"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from al_wazeer.messages.models import Message
from al_wazeer.messages.serializers import HyperLinkedMessageSerializer
from al_wazeer.mixins import OwnerMixin
from al_wazeer.permissions import IsOwner


# Create your views here.
class MessageViewSet(OwnerMixin, ModelViewSet):
    """Create, read, update and delete Messages"""

    queryset = Message.objects.prefetch_related("chat")
    serializer_class = HyperLinkedMessageSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    search_fields = ("content",)
    ordering_fields = ("created_at", "updated_at")
    filterset_fields = ("id", "chat", "assistant", "is_starred")
