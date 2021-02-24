from django.urls import path
from . import views


urlpatterns = [
    path(route = 'v1/services/rooms/start', view = views.create_room, name = 'create room'),
    path(route ='v1/services/rooms', view = views.room, name = 'room'),
]

app_name = 'api'