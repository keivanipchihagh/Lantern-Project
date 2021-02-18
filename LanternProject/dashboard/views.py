from django.shortcuts import render
from core.models import CoreSession as Session


def index(request):
    return render(request = request, context = {}, template_name = 'dashboard/index.html')


def onload_chatroom(request, user_key):
    
    # Sessions
    open_sessions, assigned_sessions = get_sessions(user_key = user_key)
    
    return render(request = request, context = {'open_sessions': open_sessions, 'assigned_sessions': assigned_sessions}, template_name = 'dashboard/chatroom.html')












# -------------------------------------------------------------- Methods --------------------------------------------------------------

def get_sessions(user_key):

    open_sessions = Session.objects.filter(status = 'open')                     # Fetch open sessions
    assigned_sessions = open_sessions.filter(user_id__user_key = user_key)      # Query assigned sessions

    return open_sessions, assigned_sessions     # Return QuerySets