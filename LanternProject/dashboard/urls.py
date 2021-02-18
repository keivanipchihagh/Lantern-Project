from django.urls import path
from . import views


urlpatterns = [
    path(route = 'v1/', view = views.index, name = 'index'),
    path(route = 'v1/serice', view = views.service, name = 'service')
]
