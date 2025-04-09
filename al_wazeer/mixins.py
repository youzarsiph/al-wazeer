"""Mixins"""


# Create your mixins here.
class OwnerMixin:
    """Filters the queryset by user and adds the owner of the object"""

    def get_queryset(self):
        """Filter queryset by user"""

        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        """Add the user to model"""

        serializer.save(user=self.request.user)
