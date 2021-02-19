from django.http.response import HttpResponse
from django.shortcuts import render
from core.models import CoreSession as Session
from core.models import CoreUser as User
from core.models import CoreMessage as Message
import json


def index(request):
    return render(request = request, context = {}, template_name = 'dashboard/index.html')


def onload_chatroom(request, user_key):
    
    # Sessions
    open_sessions, assigned_sessions = get_sessions(user_key = user_key)
    
    return render(request = request, context = {'open_sessions': open_sessions, 'assigned_sessions': assigned_sessions}, template_name = 'dashboard/chatroom.html')


def fetch_session(request):

    # Get request data
    session_key, user_key = request.GET['session_key'], request.GET['user_key']    

    # Verification
    user_id = User.objects.get(user_key = user_key).id
    session_id = Session.objects.get(session_key = session_key, user_id = user_id).id
    messages = Message.objects.filter(session_id = session_id)
    
    dictionaries = [str(obj.as_dict()) for obj in messages]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')    # Serialized response


def close_session(request):

    # Get request data
    session_key, user_key = request.GET['session_key'], request.GET['user_key']

    # Verification
    user_id = User.objects.get(user_key = user_key).id
    session_id = Session.objects.get(session_key = session_key, user_id = user_id).id

    # Close session
    session = Session.objects.get(id = session_id)
    session.status = 'closed'
    session.save()

    # Remove messages for the session
    Message.objects.filter(session_id = session_id).delete()

    # Return empty response
    return HttpResponse('')


# -------------------------------------------------------------- Methods --------------------------------------------------------------

def get_sessions(user_key):

    open_sessions = Session.objects.filter(status = 'open')                     # Fetch open sessions
    assigned_sessions = open_sessions.filter(user_id__user_key = user_key)      # Query assigned sessions

    return open_sessions, assigned_sessions     # Return QuerySets