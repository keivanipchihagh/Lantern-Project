from django.urls import path
from . import views


urlpatterns = [

    # SignIn Section
    path(route = 'signin', view = views.signin, name = 'signin'),

    # Index Section
    path(route = 'v1/user/<int:user_key>', view = views.index, name = 'index'),

    # Profile Section
    path(route = 'v1/user/<int:user_key>/profile/pi', view = views.profile_update_pi, name = 'update personal information'),

    # Chatroom Setion
    path(route = 'v1/fetch/session', view = views.fetch_session, name = 'fetch session'),
    path(route = 'v1/close/session', view = views.close_session, name = 'close session'),
    path(route = 'v1/star/session', view = views.star_session, name = 'star session'),    
]
