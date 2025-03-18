"""Views for al_wazeer.assistants"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from al_wazeer.assistants.models import Assistant
from al_wazeer.assistants.serializers import AssistantSerializer


# Create your views here.
class AssistantViewSet(ModelViewSet):
    """Create, read, update and delete Assistants (admins only)"""

    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    filterset_fields = ("id", "model")
    search_fields = ("name", "model", "description")
    ordering_fields = ("name", "created_at", "updated_at")

    def get_permissions(self):
        """Allow read only access for users"""

        if self.action in ("list", "retrieve"):
            self.permission_classes = (IsAuthenticated,)

        return super().get_permissions()
