from django import VERSION
from django.urls import path
from . import views
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [

    # Authentication
    path(route = 'login', view = views.login, name = 'login'),
    path(route = 'logout', view = LogoutView.as_view(), kwargs = {'next_page': settings.LOGOUT_REDIRECT_URL}, name = 'logout'),

    # Index Section
    path(route = 'v1/user/<str:username>', view = views.dashboard, name = 'dashboard'),
    path(route = 'v1/user/<str:username>/notifications/markasread', view = views.mark_notification, name = 'mark_notification'),

    # Profile Section
    path(route = 'v1/user/<str:username>/profile/update', view = views.profile_update, name = 'update personal information'),

    # Reserved Messages Section
    path(route = 'v1/user/<str:username>/reversedmessages/messages/modify', view = views.reversedmessages_modify, name = 'update|delete reserved message'),

    # Chatroom Setion
    path(route = 'v1/user/<str:username>/chatroom/assign_room', view = views.chatroom_assign_room, name = 'assign a room'),
    path(route = 'v1/user/<str:username>/chatroom/close_room', view = views.chatroom_close_room, name = 'close a room'),
]
