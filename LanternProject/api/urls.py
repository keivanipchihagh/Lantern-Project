from django.urls import path
from . import views


urlpatterns = [
    path(route = 'sessions/start', view = views.create_session, name = 'create session'),
    path(route ='session/<str:room_name>/', view = views.room, name = 'room'),
]