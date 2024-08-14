""" URL Configuration for botland """

from django.urls import path, include


# Create your URLConf here.
urlpatterns = [
    path("", include("botland.bots.urls")),
    path("", include("botland.chats.urls")),
    path("", include("botland.messages.urls")),
]
