from django.shortcuts import render

def template(request):
    return render(request = request, context = {}, template_name = 'api/template.html')

def index(request):
    return render(request = request, context = {}, template_name =  'api/index.html')

def room(request, room_name):
    return render(request = request, context = {'room_name': room_name}, template_name = 'api/room.html')