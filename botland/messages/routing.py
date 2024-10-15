""" Routing for botland.messages """

from django.urls import re_path
from botland.messages.consumers import AsyncMessageConsumer


# Create your routing here.
websocket_urlpatterns = [
    re_path(r"chat/(?P<chat>\w+)/$", AsyncMessageConsumer.as_asgi()),
]
