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
    path(route = 'v1/fetch/room', view = views.fetch_room, name = 'fetch room'),
    path(route = 'v1/close/room', view = views.close_room, name = 'close room'),
]
