from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from core.models import CoreSession as Session
from core.models import CoreUser as User
from core.models import CoreMessage as Message
from core.models import CoreSite as Site
from core.models import CoreLog as Log
from .models import DashboardMenu as Menu
import json
from .forms import ProfileForm, LoginForm
from django.views.decorators.http import require_http_methods   # Request restrictions
from django.urls import reverse
from datetime import datetime, timedelta


##################################################################### Login ##############################################################################

@require_http_methods(['GET', 'POST'])
def signin(request):

    if request.method == 'GET':
        return render(request = request, context = {'form': LoginForm(auto_id = True, initial = {'email': '', 'password': ''})}, template_name = 'dashboard/signin.html')
    else:
        form = LoginForm(request.POST)

        if form.is_valid():
            try:
                # Get user if exists
                user = User.objects.get(email = form.cleaned_data['email'], password = form.cleaned_data['password'])

                # Log
                Log(title = 'Sign In', user_id = user.id, site_id = user.site_id).save()

                return HttpResponseRedirect('v1/user/' + user.user_key)
            except:
                return render(request = request, context = {'form': LoginForm(auto_id = True, initial = {'email': form.cleaned_data['email'], 'password': ''}), 'message': 'Invalid Email/Password'}, template_name = 'dashboard/signin.html')
        else:
            return HttpResponseForbidden(form.errors.values())
            
##################################################################### Index ##############################################################################

@require_http_methods(['GET'])
def index(request, user_key):
    
    user = User.objects.get(user_key = user_key)
    other_users = User.objects.filter(site_id = user.site_id).exclude(id = user.id)
    sitename = Site.objects.get(id = user.site_id).name
    log = Log.objects.filter(user_id = user.id).latest('datetime')
    menu = Menu.objects.filter(category = 'Shared')

    # Data for home.html
    home = {
        'firstname': user.firstname,
        'lastname': user.lastname,
        'sitename': sitename,
        'role': user.role,
        'sitename': sitename,
    }

    # Data for aside.html
    aside = {
        'menu': menu,
    }

    # Data for header.html
    header = {
        'username': user.username,                
        'role': user.role,
    }

    # Data for profile.html
    profile = {
        'firstname': user.firstname,
        'lastname': user.lastname,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'sitename': sitename,
        'country': user.country,
        'city': user.city,        
        'bio': user.bio,
        'rating': user.rating,
        'last_login': log.datetime,
        'activities': len(Session.objects.filter(user_id = user.id)),
        'other_users': other_users,        
        'form': ProfileForm(auto_id = True, instance = user),
    }

    # Data for index.html
    data = {        
        'profile': profile,                 # Data for profile.html
        'aside': aside,                     # Data for aside.html
        'home': home,                       # Data for home.html
        'header': header,                   # Data for header.html
        'page': request.GET.get('page'),
        'user_key': user.user_key,
        'title': request.GET.get('page'),
    }

    return render(request = request, context = data, template_name = 'dashboard/index.html')

##################################################################### Profile ##############################################################################

@require_http_methods(['POST'])
def profile_update_pi(request, user_key):

    form = ProfileForm(request.POST, request.FILES)

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

        return HttpResponse('Updated, Reloading...')
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
