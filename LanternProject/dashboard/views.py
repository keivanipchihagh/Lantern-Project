from django.shortcuts import render
from core.models import CoreSession as Session
from datetime import datetime
from django.http import HttpResponse


def index(request):
    return render(request = request, context = {}, template_name = 'dashboard/index.html')


def service(request, user_key):
    
    open_sessions = Session.objects.filter(status = 'open')                     # Fetch all open sessions
    assigned_sessions = open_sessions.filter(user_id__user_key = user_key)      # Query all assigned sessions

    return render(request = request, context = {'open_sessions': open_sessions, 'assigned_sessions': assigned_sessions}, template_name = 'dashboard/chatroom.html')