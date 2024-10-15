""" URL Configuration for botland """

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from botland.bots.views import BotViewSet
from botland.chats.views import ChatViewSet
from botland.messages.views import MessageViewSet


# Create your URLConf here.
router = DefaultRouter()
router.register("bots", BotViewSet, "bot")
router.register("chats", ChatViewSet, "chat")
router.register("messages", MessageViewSet, "message")

urlpatterns = [
    path("", include(router.urls)),
]
