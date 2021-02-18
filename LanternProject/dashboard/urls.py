from django.urls import path
from . import views


urlpatterns = [
    path(route = 'v1/', view = views.index, name = 'index'),
    path(route = 'v1/chatroom/<int:user_key>', view = views.onload_chatroom, name = 'chatroom'),
]
