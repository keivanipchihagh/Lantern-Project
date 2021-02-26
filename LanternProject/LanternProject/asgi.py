"""
ASGI config for LanternProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.conf.urls import url
import api.consumers, dashboard.consumers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LanternProject.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        # URLRouter(
        #     api.routing.websocket_urlpatterns,
        # )
        URLRouter([
            url(r'ws/rooms/(?P<room_name>\w+)/$', api.consumers.ChatConsumer.as_asgi()),    # API | Dashboard
            url(r'ws/halls/(?P<hall_name>\w+)/$', dashboard.consumers.ChatConsumer.as_asgi()),    # Dashboard | Database
        ])
    ),
})