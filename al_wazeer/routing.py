""" Routing for al_wazeer.messages """

from django.urls import re_path

from al_wazeer.messages.consumers import MessageConsumer


# Create your routing here.
websocket_urlpatterns = [
    re_path(r"chat/(?P<chat>\w+)/$", MessageConsumer.as_asgi()),
]
