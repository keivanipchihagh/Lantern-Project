from django.http import response
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import render
import secrets
from datetime import datetime
import json

from django.views.decorators.http import require_http_methods

# Core Models
from core.models import CoreSite as Site
from core.models import CoreRoom as Room
from core.models import CoreUser as User
from core.models import CoreCustomization as Customization


def room(request):
    return render(request=request, context={}, template_name='api/template.html')


@require_http_methods(['GET'])
def service(request, site_name):

    response = HttpResponse('')

    if request.GET.get('action') == 'initialize':
        response = initialize(site_name, request.GET.get('apikey'))


    return response


def create_room(request):

    try:
        # Get site entry
        site = Site.objects.get(url=request.META['HTTP_HOST'])

        # Check key authenticity
        if site.public_key == request.GET['key']:

            # Room properties
            room_key = secrets.token_hex(16)
            status = 'open'
            date_opened = datetime.now()
            user_id = 1
            site_id = site.id

            # Save Room
            Room(room_key=room_key, status=status, date_opened=date_opened,
                 user_id=user_id, site_id=site_id).save()

            return HttpResponse(room_key)            # Return room key
        else:
            return HttpResponseForbidden()              # Invalid API key

    except Site.DoesNotExist:   # Request URL match not found in database
        return HttpResponseBadRequest()

# ------------------------------------------------------------------------  Methods ------------------------------------------------------------------------

def initialize(name, public_key):

    try: site_id = Site.objects.get(name = name, public_key = public_key).id
    except:
        response = JsonResponse({"msg": "Access Denied"})
        response.status_code = 403
        return response

    try:

        customization = Customization.objects.get(site_id = site_id)

        return JsonResponse({
            'livechat': {
                'service': True if (User.objects.filter(site_id = site_id, is_online = True).count() > 0) else False,
                'title': customization.livechat_title,
                'placeholder': customization.livechat_placeholder_online,
            },
            'virtualagent': {
                'service': True,
                'title': customization.ticket_title,
                'placeholder': customization.ticket_placeholder,
            },
            'ticket': {
                'service': True,
                'title': customization.virtualagent_title,
                'placeholder': customization.virtualagent_placeholder,
            }
        })

    except:
        response = JsonResponse({"msg": "Server Unavailable"})
        response.status_code = 503
        return response