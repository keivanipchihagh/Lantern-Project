from django.urls import path
from . import views


urlpatterns = [
    path(route = '', view = views.index, name = 'index'),
    path(route ='session/<str:room_name>/', view = views.room, name = 'room'),
]