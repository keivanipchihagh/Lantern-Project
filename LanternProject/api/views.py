# Django packages
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render

# Core Models
from core.models import CoreSite as Site


def index(request):
    return render(request = request, context = {}, template_name =  'api/index.html')


def room(request, room_name):
    return render(request = request, context = {'room_name': room_name}, template_name = 'api/room.html')


def create_session(request):
    
    URL = request.META['HTTP_HOST']    

    try:
        site_ref = Site.objects.get(url = URL)

        if site_ref.public_key == request.GET['key']:
            return HttpResponse(request.GET['key'])
        else:
            return HttpResponseForbidden()     # Invalid API key

    except Site.DoesNotExist:   # Request URL match not found in database
        return HttpResponseBadRequest()

    