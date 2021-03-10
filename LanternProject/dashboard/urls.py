from django import VERSION
from django.urls import path
from . import views


urlpatterns = [

    # SignIn Section
    path(route = 'login', view = views.login, name = 'login'),

    # Index Section
    path(route = 'v1/user/<str:username>', view = views.dashboard, name = 'dashboard'),

    # Profile Section
    path(route = 'v1/user/<str:username>/profile/update', view = views.profile_update, name = 'update personal information'),

    # Reserved Messages Section
    path(route = 'v1/user/<str:username>/reversedmessages/messages/modify', view = views.reversedmessages_modify, name = 'update|delete reserved message'),

    # Chatroom Setion
    path(route = 'v1/user/<str:username>/chatroom/assign_room', view = views.chatroom_assign_room, name = 'assign a room'),
    path(route = 'v1/user/<str:username>/chatroom/close_room', view = views.chatroom_close_room, name = 'close a room'),
]
