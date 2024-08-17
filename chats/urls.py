""" URL Configuration for botland.chats """

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from botland.messages.views import ChatMessagesViewSet


# Create your URLConf here.
router = DefaultRouter()
router.register("messages", ChatMessagesViewSet, "message")

urlpatterns = [
    path("chats/<int:id>/", include((router.urls, "messages"), "messages")),
]
