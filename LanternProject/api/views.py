from os import stat
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
import secrets
from datetime import datetime

# Core Models
from core.models import CoreSite as Site
from core.models import CoreSession as Session


def room(request):
    return render(request = request, context = {}, template_name = 'api/room.html')


def create_session(request):

    try:
        # Get site entry
        site = Site.objects.get(url = request.META['HTTP_HOST'])        

        # Check key authenticity
        if site.public_key == request.GET['key']:        

            # Session properties
            session_key = secrets.token_hex(16)
            status = 'open'
            date_opened = datetime.now()
            user_id = 2
            site_id = site.id
            
            # Save session
            Session(session_key = session_key, status = status, date_opened = date_opened, user_id = user_id, site_id = site_id).save()

            return HttpResponse(session_key)            # Return session key
        else:
            return HttpResponseForbidden()              # Invalid API key

    except Site.DoesNotExist:   # Request URL match not found in database
        return HttpResponseBadRequest()