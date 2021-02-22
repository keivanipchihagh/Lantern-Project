from django.urls import path
from . import views


urlpatterns = [
    path(route = '', view = views.index, name = 'index')
]

app_name = 'core'