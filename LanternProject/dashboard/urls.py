from django.urls import path
from . import views


urlpatterns = [

    # Sign In
    path(route = 'signin', view = views.signin, name = 'signin'),

    # Index
    path(route = 'v1/user/<int:user_key>', view = views.index, name = 'index'),    

    path(route = 'v1/chatroom/<int:user_key>', view = views.onload_chatroom, name = 'chatroom'),
    path(route = 'v1/fetch/session', view = views.fetch_session, name = 'fetch session'),
    path(route = 'v1/close/session', view = views.close_session, name = 'close session'),
    path(route = 'v1/star/session', view = views.star_session, name = 'star session'),

    # Profile section
    path(route = 'v1/profile/<int:user_key>', view = views.profile, name = 'profile'),
    path(route = 'v1/profile/<int:user_key>/update/pi', view = views.profile_update_pi, name = 'update personal information')
]
