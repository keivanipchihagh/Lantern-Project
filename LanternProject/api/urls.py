from django.urls import path
from . import views


urlpatterns = [
    path(route = 'v1/services/sessions/start', view = views.create_session, name = 'create session'),
    path(route ='v1/services/sessions', view = views.room, name = 'room'),
]

app_name = 'api'