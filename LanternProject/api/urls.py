from django.urls import path
from . import views


urlpatterns = [
    path(route = 'ui/template', view = views.template, name = 'UI'),
    path(route = '', view = views.index, name = 'index'),
    path(route ='session/<str:room_name>/', view = views.room, name = 'room'),
]