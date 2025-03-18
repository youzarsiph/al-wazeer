"""Generic View Mixins"""

from typing import Any
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse


# Create your mixins here.
class AdminUserMixin(UserPassesTestMixin):
    """Check if the user is an admin"""

    def test_func(self) -> bool | None:
        return self.request.user.is_staff


class AccountOwnerMixin(UserPassesTestMixin):
    """Check if the user is owner of the account"""

    def test_func(self) -> bool | None:
        return self.request.user == self.get_object()


class ExtraContextMixin:
    """Passes extra context to templates"""

    extra_context = {}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return {**super().get_context_data(**kwargs), **self.extra_context}


class UserFilterMixin:
    """Filters queryset by user"""

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(user_id=self.request.user.pk)


class OwnerMixin:
    """Adds the owner automatically"""

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Add the owner of the object automatically"""

        object = form.save(commit=False)
        object.user = self.request.user

        return super().form_valid(form)
