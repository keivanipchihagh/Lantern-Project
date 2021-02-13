from django.http.response import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request = request, context = {}, template_name =  'api/index.html')


def room(request, room_name):
    return render(request = request, context = {'room_name': room_name}, template_name = 'api/room.html')


def create_session(request):
    return HttpResponse(request.GET['key'])