from django.urls import path
from . import views


urlpatterns = [

    # SignIn Section
    path(route = 'signin', view = views.signin, name = 'signin'),

    # Index Section
    path(route = 'v1/user/<int:user_key>', view = views.index, name = 'index'),

    # Profile Section
    path(route = 'v1/user/<int:user_key>/profile/update', view = views.profile_update, name = 'update personal information'),

    # Chatroom Setion
    path(route = 'v1/user/<int:user_key>/chatroom/assign_room', view = views.chatroom_assign_room, name = 'assign a room'),
    path(route = 'v1/user/<int:user_key>/chatroom/close_room', view = views.chatroom_close_room, name = 'close a room'),
]
