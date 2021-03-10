from django.urls import path
from . import views


urlpatterns = [
    path(route = 'v1/hosts/<str:host>', view = views.index, name = 'index'),
    path(route = 'v1/hosts/<str:host>/services/rooms/start', view = views.start, name = 'start'),
]

app_name = 'api'