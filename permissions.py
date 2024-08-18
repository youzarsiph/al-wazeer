""" Custom access permissions """

from rest_framework.permissions import BasePermission


# Create your permissions here.
class IsOwner(BasePermission):
    """Allow access to the owner of the object"""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsAccountOwner(BasePermission):
    """Allow access to the owner of the user account"""

    def has_object_permission(self, request, view, obj):
        return request.user == obj
