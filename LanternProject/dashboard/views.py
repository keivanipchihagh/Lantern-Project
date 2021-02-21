from django.http.response import HttpResponse
from django.shortcuts import render
from core.models import CoreSession as Session
from core.models import CoreUser as User
from core.models import CoreMessage as Message
from core.models import CoreSite as Site
import json
from .forms import Profile
from django.views.decorators.http import require_http_methods   # Request restrictions


##################################################################### Index ##############################################################################


def index(request, user_key):
    return render(request = request, context = {}, template_name = 'dashboard/index.html')


##################################################################### Profile ##############################################################################

@require_http_methods(['GET'])
def profile(request, user_key):

    user = User.objects.get(user_key = user_key)
    sitename = Site.objects.get(id = user.site_id).name
    other_users = User.objects.filter(site_id = user.site_id).exclude(id = user.id)

    # Data for initial form fields and other attributes
    data = {
        'firstname': user.firstname,
        'lastname': user.lastname,
        'username': user.username,
        'email': user.email,
        'phonenumber': user.phonenumber,
        'role': user.role,
        'site': sitename,
        'country': user.country,
        'city': user.city,        
        'bio': user.bio,
        'rating': user.rating,
        'activities': len(Session.objects.filter(user_id = user.id)),
        'other_users': other_users,
        'user_key': user.user_key,
    }

    return render(request = request, context = {'form': Profile(auto_id = True, instance = user), 'data': data}, template_name = 'dashboard/profile.html')


@require_http_methods(['POST'])
def profile_update_pi(request, user_key):

    form = Profile(request.POST, request.FILES)

    if form.is_valid():
        User.objects.filter(user_key = user_key).update(
            firstname = form.cleaned_data.get('firstname'),
            lastname = form.cleaned_data.get('lastname'),
            phonenumber = form.cleaned_data.get('phonenumber'),
            country = form.cleaned_data.get('country'),
            city = form.cleaned_data.get('city'),
            bio = form.cleaned_data.get('bio'),
        )
        # form.save()

        return HttpResponse('Updated!')
    else:
        return HttpResponse(form.errors.as_text())  # Validation failed

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