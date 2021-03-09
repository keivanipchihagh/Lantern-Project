from django.http import response
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
import secrets
from datetime import datetime

from django.views.decorators.http import require_http_methods

# Core Models
from core.models import CoreSite as Site
from core.models import CoreRoom as Room
from core.models import CoreUser as User

# API Models
from .models import ApiTitle as Title


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
            user_id = 1,
            site_id = site.id
        )
        room.save()

        return HttpResponse(room.room_key)

    except Site.DoesNotExist:   # Request URL match not found in database
        return HttpResponseForbidden('Server refused to connect.')
    except:
        return HttpResponseBadRequest()
        
@require_http_methods(['GET'])
def service(request, site_name):

    response = HttpResponse('')

    if request.GET.get('action') == 'initialize':
        response = initialize(site_name, request.GET.get('apikey'))

    return response


# ------------------------------------------------------------------------  Methods ------------------------------------------------------------------------

def initialize(name, public_key):

    try: site = Site.objects.get(name = name, public_key = public_key)
    except:
        response = JsonResponse({"msg": "Access Denied"})
        response.status_code = 403
        return response

    try:
        customization = Customization.objects.get(site_id = site.id)

        return JsonResponse({
            'app': {
                'title': customization.title,
                'placeholder': customization.placeholder,
                'formtitles': ','.join([str(item.title) for item in Title.objects.filter(customization_id = customization.id)]),
            },
            'options': [
                {
                    'service': True if (User.objects.filter(site_id = site.id, is_online = True).count() > 0 and site.livechat_service) else False,
                    'title': customization.livechat_title,
                    'placeholder': customization.livechat_placeholder,
                },
                {
                    'service': site.ticket_service,
                    'title': customization.ticket_title,
                    'placeholder': customization.ticket_placeholder,
                },
                {
                    'service': site.virtualagent_service,
                    'title': customization.virtualagent_title,
                    'placeholder': customization.virtualagent_placeholder,    
                }
            ],            
        })

    except:
        response = JsonResponse({"msg": "Server Unavailable"})
        response.status_code = 503
        return response