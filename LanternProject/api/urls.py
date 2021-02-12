from django.urls import path
from . import views


urlpatterns = [
    path(route = '', view = views.index, name = 'index'),
    path(route ='<str:room_name>/', view = views.room, name = 'room'),
]