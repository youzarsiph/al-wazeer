"""Views for al_wazeer.ui"""

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic

from al_wazeer.assistants.models import Assistant
from al_wazeer.chats.models import Chat
from al_wazeer.messages.models import Message
from al_wazeer.ui import mixins
from al_wazeer.ui.forms import UserCreateForm


# User model
User = get_user_model()


# Create your views here.
class IndexView(generic.TemplateView):
    """Home page"""

    template_name = "ui/index.html"


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    """Profile page"""

    template_name = "registration/profile.html"


# User views
class SignupView(SuccessMessageMixin, generic.CreateView):
    """Creates a user"""

    model = User
    form_class = UserCreateForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("al-wazeer:profile")
    success_message = "Your account was created successfully!"


class UserUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    mixins.AccountOwnerMixin,
    mixins.ExtraContextMixin,
    generic.UpdateView,
):
    """Updates a user"""

    model = User
    template_name = "registration/form.html"
    fields = ["first_name", "last_name", "email"]
    success_url = reverse_lazy("al-wazeer:profile")
    success_message = "Your account was updated successfully!"
    extra_context = {"title": "Update Account"}


class UserDeleteView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    mixins.AccountOwnerMixin,
    mixins.ExtraContextMixin,
    generic.DeleteView,
):
    """Deletes a user"""

    model = User
    template_name = "registration/form.html"
    success_url = reverse_lazy("al-wazeer:index")
    success_message = "Your account was deleted successfully!"
    extra_context = {
        "title": "Delete Account",
        "description": "Are you sure that you want to delete your account?",
    }


# Assistant views
class AssistantCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    mixins.AdminUserMixin,
    mixins.ExtraContextMixin,
    generic.CreateView,
):
    """Create a new Assistant"""

    model = Assistant
    template_name = "ui/assistant/form.html"
    fields = ["name", "model", "description"]
    success_url = reverse_lazy("al-wazeer:assistants")
    success_message = "Assistant '%(name)s' was created successfully!"
    extra_context = {
        "title": "New Assistant",
        "assistant_list": Assistant.objects.all(),
    }


class AssistantListView(LoginRequiredMixin, mixins.ExtraContextMixin, generic.ListView):
    """View list of Assistants"""

    model = Assistant
    template_name = "ui/assistant/base.html"


class AssistantDetailView(LoginRequiredMixin, generic.DetailView):
    """View details of an Assistant"""

    model = Assistant
    template_name = "ui/assistant/id.html"
    extra_context = {"assistant_list": Assistant.objects.all()}


class AssistantUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    mixins.AdminUserMixin,
    mixins.ExtraContextMixin,
    generic.UpdateView,
):
    """Update an Assistant"""

    model = Assistant
    template_name = "ui/assistant/form.html"
    fields = ["name", "model", "description"]
    success_url = reverse_lazy("al-wazeer:assistants")
    success_message = "Assistant '%(name)s' was updated successfully!"
    extra_context = {
        "title": "Update Assistant",
        "assistant_list": Assistant.objects.all(),
    }


class AssistantDeleteView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    mixins.AdminUserMixin,
    mixins.ExtraContextMixin,
    generic.DeleteView,
):
    """Delete an Assistant"""

    model = Assistant
    template_name = "ui/assistant/form.html"
    success_url = reverse_lazy("al-wazeer:assistants")
    success_message = "Assistant was deleted successfully!"
    extra_context = {
        "title": "Delete Assistant",
        "assistant_list": Assistant.objects.all(),
    }


# Chat views
class ChatCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    mixins.OwnerMixin,
    mixins.ExtraContextMixin,
    generic.CreateView,
):
    """Create a new chat"""

    model = Chat
    template_name = "ui/chat/form.html"
    success_url = reverse_lazy("al-wazeer:chats")
    success_message = "Chat '%(title)s' was created successfully!"
    fields = ["assistant", "title", "description", "role", "is_pinned"]
    extra_context = {"title": "New Chat", "description": "Create new chat"}


class ChatListView(LoginRequiredMixin, generic.TemplateView):
    """View list of Chats"""

    template_name = "ui/chat/base.html"


class ChatDetailView(LoginRequiredMixin, mixins.UserFilterMixin, generic.DetailView):
    """View details of a chat"""

    model = Chat
    template_name = "ui/chat/id.html"


class ChatUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    mixins.UserFilterMixin,
    mixins.ExtraContextMixin,
    generic.UpdateView,
):
    """Update a Chat"""

    model = Chat
    template_name = "ui/chat/form.html"
    success_url = reverse_lazy("al-wazeer:chats")
    success_message = "Chat '%(title)s' was updated successfully!"
    fields = ["assistant", "title", "description", "role", "is_pinned"]
    extra_context = {"title": "Update chat", "description": "Update this chat"}


class ChatDeleteView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    mixins.UserFilterMixin,
    mixins.ExtraContextMixin,
    generic.DeleteView,
):
    """Delete a Chat"""

    model = Chat
    template_name = "ui/chat/form.html"
    success_url = reverse_lazy("al-wazeer:chats")
    success_message = "Chat was deleted successfully!"
    extra_context = {
        "title": "Delete chat",
        "description": "Are you sure that you want to delete this chat?",
    }


# Message views
class MessageUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    mixins.UserFilterMixin,
    mixins.ExtraContextMixin,
    generic.UpdateView,
):
    """Update a Message"""

    model = Message
    template_name = "ui/form.html"
    success_message = "Message was updated successfully!"
    fields = ["content", "is_starred"]
    extra_context = {"title": "Update Message", "description": "Update this message"}


class MessageDeleteView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    mixins.UserFilterMixin,
    mixins.ExtraContextMixin,
    generic.DeleteView,
):
    """Delete a Message"""

    model = Message
    template_name = "ui/form.html"
    success_message = "Message was deleted successfully!"
    extra_context = {
        "title": "Delete Message",
        "description": "Are you sure that you want to delete this message?",
    }
