""" Views for botland.bots """

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from botland.bots.models import Bot
from botland.bots.serializers import BotSerializer


# Create your views here.
class BotViewSet(ModelViewSet):
    """Bot ViewSet"""

    queryset = Bot.objects.all()
    serializer_class = BotSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ("id", "slug")
    search_fields = ("name", "slug", "description")
    ordering_fields = ("id", "name", "created_at", "updated_at")
