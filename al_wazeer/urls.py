""" URL Configuration for al_wazeer """

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from al_wazeer.assistants.views import AssistantViewSet
from al_wazeer.chats.views import ChatViewSet
from al_wazeer.messages.views import MessageViewSet


# Create your URLConf here.
router = DefaultRouter()
router.register("assistants", AssistantViewSet, "assistant")
router.register("chats", ChatViewSet, "chat")
router.register("messages", MessageViewSet, "message")

urlpatterns = [
    path("", include(router.urls)),
]
