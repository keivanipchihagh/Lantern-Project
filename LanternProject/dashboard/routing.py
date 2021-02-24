from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/halls/(?P<hall_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]