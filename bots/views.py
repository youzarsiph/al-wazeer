""" Views for botland.bots """

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from botland.bots.models import Bot
from botland.bots.serializers import BotSerializer


# Create your views here.
class BotViewSet(ModelViewSet):
    """Bot ViewSet"""

    queryset = Bot.objects.all()
    serializer_class = BotSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    filterset_fields = ("id", "model")
    search_fields = ("name", "model", "description")
    ordering_fields = ("id", "name", "created_at", "updated_at")

    def get_permissions(self):
        """Allow read only access for users and read/write access to staffs"""

        if self.action in ("list", "retrieve"):
            self.permission_classes = (IsAuthenticated,)

        return super().get_permissions()
