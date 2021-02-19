from django.http.response import HttpResponse
from django.shortcuts import render
from core.models import CoreSession as Session
from core.models import CoreUser as User
from core.models import CoreMessage as Message
import json


def index(request):
    return render(request = request, context = {}, template_name = 'dashboard/index.html')


################################################################### Profile ##############################################################################

def profile(request, user_key):

    user = User.objects.get(user_key = user_key)
    other_users = User.objects.filter(site_id = user.site_id).exclude(id = user.id)

    data = {
        'firstname': user.firstname,
        'lastname': user.lastname,
        'username': user.username,
        'phonenumber': user.phonenumber,
        'country': user.country,
        'city': user.city,
        'role': user.role,
        'bio': user.bio,
        'rating': user.rating,
        'activities': len(Session.objects.filter(user_id = user.id)),
        'other_users': other_users,
        'last_login': user.last_login
    }

    return render(request = request, context = {'data': data}, template_name = 'dashboard/profile.html')

################################################################### Chatroom #############################################################################

def onload_chatroom(request, user_key):
    
    # Sessions
    open_sessions, assigned_sessions, starred_sessions = get_sessions(user_key = user_key)
    
    return render(request = request, context = {'open_sessions': open_sessions, 'assigned_sessions': assigned_sessions, 'starred_sessions': starred_sessions}, template_name = 'dashboard/chatroom.html')


def fetch_session(request):

    # Get request data
    session_key, user_key = request.GET['session_key'], request.GET['user_key']    

    # Verification
    user_id = User.objects.get(user_key = user_key).id
    session_id = Session.objects.get(session_key = session_key, user_id = user_id).id
    messages = Message.objects.filter(session_id = session_id)
    
    # Format messages
    dictionaries = [str(obj.as_dict()) for obj in messages]

    # Return serialized response
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


def close_session(request):

    # Get request data
    session_key, user_key = request.GET['session_key'], request.GET['user_key']

    # Verification
    user_id = User.objects.get(user_key = user_key).id
    session_id = Session.objects.get(session_key = session_key, user_id = user_id).id

    # Update session - Close
    session = Session.objects.get(id = session_id)
    session.status = 'closed'
    session.save()

    # Remove messages for the session
    Message.objects.filter(session_id = session_id).delete()

    # Return empty response
    return HttpResponse('')


def star_session(request):

    # Get request data
    session_key, user_key = request.GET['session_key'], request.GET['user_key']

    # Verification
    user_id = User.objects.get(user_key = user_key).id
    session_id = Session.objects.get(session_key = session_key, user_id = user_id).id

    # Update session - Star
    session = Session.objects.get(id = session_id)
    session.starred = 0 if (session.starred) else 1
    session.save()

    # Return empty response
    return HttpResponse('')


# -------------------------------------------------------------- Methods --------------------------------------------------------------

def get_sessions(user_key):

    open_sessions = Session.objects.filter(status = 'open')                     # Fetch open sessions
    assigned_sessions = open_sessions.filter(user_id__user_key = user_key)      # Query assigned sessions
    starred_sessions = open_sessions.filter(starred = True)                     # Query starred sessions

    return open_sessions, assigned_sessions, starred_sessions                   # Return QuerySets