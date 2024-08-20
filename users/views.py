""" Views for botland.users """

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from botland.users.models import User
from botland.users.serializers import UserSerializer


# Create your views here.
class UserViewSet(ReadOnlyModelViewSet):
    """User ViewSet"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    filterset_fields = ("id", "username")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering_fields = ("id", "username", "date_joined", "last_login")
