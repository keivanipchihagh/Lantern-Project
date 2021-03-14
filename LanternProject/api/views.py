from django.http import response
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
import secrets
from datetime import datetime

from django.views.decorators.http import require_http_methods

# Core Models
from dashboard.models import Site
from dashboard.models import Room


@require_http_methods(['GET'])
def index(request, host):
    ''' Authenticates & loads the initial template '''
    
    try:
        # Check site name, url, key for authentication
        Site.objects.get(host = host, url = request.META['HTTP_HOST'], public_key = request.GET.get('token'))

        return render(request = request, context = {}, template_name = 'api/template.html')
    except Site.DoesNotExist:
        return HttpResponseForbidden('Forbidden')


def start(request, host):
    ''' Authenticates & creates a room, then returns the room_key to the socket end-point '''

    try:
        # Check authenticity
        site = Site.objects.get(host = host, url = request.META['HTTP_HOST'], public_key = request.GET.get('token'))

        # Save Room
        room = Room (
            room_key = secrets.token_hex(16),
            status = 'open',
            date_opened = datetime.now(),
            user_id = 4,
            site_id = site.id
        )
        room.save()

        return HttpResponse(room.room_key)

    except Site.DoesNotExist:   # Request URL match not found in database
        return HttpResponseForbidden('Server refused to connect.')
    except:
        return HttpResponseBadRequest()