from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect, render
from core.models import CoreRoom as Room
from core.models import CoreUser as User
from core.models import CoreMessage as Message
from core.models import CoreSite as Site
from core.models import CoreLog as Log
from .models import DashboardMenu as Menu
import json
from .forms import ProfileForm, LoginForm
from django.views.decorators.http import require_http_methods   # Request restrictions
from django.urls import reverse


# ------------------------------------------------------------------------ Signin ------------------------------------------------------------------------

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
            
# ------------------------------------------------------------------------ Index ------------------------------------------------------------------------

@require_http_methods(['GET'])
def index(request, user_key):
    
    user = User.objects.get(user_key = user_key)
    other_users = User.objects.filter(site_id = user.site_id).exclude(id = user.id)
    site = Site.objects.get(id = user.site_id)
    sitename = site.id
    hall_key = site.public_key
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
    
    # Data for chatroom
    open_rooms, assigned_rooms = get_rooms(user_key = user_key)
    chatroom = {
        'open_rooms': open_rooms,
        'assigned_rooms': assigned_rooms,
        'hall_key': hall_key,
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
        'activities': len(Room.objects.filter(user_id = user.id)),
        'other_users': other_users,        
        'form': ProfileForm(auto_id = True, instance = user),
    }

    # Data for index.html
    data = {        
        'profile': profile,                 # Data for profile.html
        'aside': aside,                     # Data for aside.html
        'home': home,                       # Data for home.html
        'header': header,                   # Data for header.html
        'chatroom': chatroom,               # Data for chatroom.html
        'page': request.GET.get('page'),
        'user_key': user.user_key,
        'title': request.GET.get('page'),
    }

    return render(request = request, context = data, template_name = 'dashboard/index.html')

# ------------------------------------------------------------------------ Profile ------------------------------------------------------------------------

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

        return HttpResponse('Updated, Reloading...')
    else:
        return HttpResponse(form.errors.as_text())  # Validation failed

# ------------------------------------------------------------------------ Chatroom ------------------------------------------------------------------------

def fetch_room(request):

    # Get request data
    room_key, user_key = request.GET['room_key'], request.GET['user_key']    

    # Verification
    user_id = User.objects.get(user_key = user_key).id
    room_id = Room.objects.get(room_key = room_key, user_id = user_id).id
    messages = Message.objects.filter(room_id = room_id)
    
    # Format messages
    dictionaries = [str(obj.as_dict()) for obj in messages]

    # Return serialized response
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


def close_room(request):

    # Get request data
    room_key, user_key = request.GET['room_key'], request.GET['user_key']

    # Verification
    user_id = User.objects.get(user_key = user_key).id
    room_id = Room.objects.get(room_key = room_key, user_id = user_id).id

    # Update room - Close
    room = Room.objects.get(id = room_id)
    room.status = 'closed'
    room.save()

    # Remove messages for the room
    Message.objects.filter(room_id = room_id).delete()

    # Return empty response
    return HttpResponse('')

# ------------------------------------------------------------------------ Methods ------------------------------------------------------------------------

def get_rooms(user_key):

    open_rooms = Room.objects.exclude(status = 'closed').order_by('-date_opened')       # Fetch open rooms
    assigned_rooms = open_rooms.filter(user_id__user_key = user_key)                    # Query assigned rooms

    return open_rooms, assigned_rooms                                                   # Return QuerySets
