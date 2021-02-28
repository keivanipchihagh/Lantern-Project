from django.http.response import Http404, HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from core.models import CoreRoom as Room
from core.models import CoreUser as User
from core.models import CoreMessage as Message
from core.models import CoreSite as Site
from core.models import CoreLog as Log
from .models import DashboardMenu as Menu
from .models import DashboardNewsLetter as NewsLetter
import json
from .forms import ProfileForm, LoginForm
from django.views.decorators.http import require_http_methods   # Request restrictions
from datetime import datetime, timedelta


# ------------------------------------------------------------------------ Errors -------------------------------------------------------------------------

def handler404(request, exception = None):
    response = render(request = request, template_name = '404.html')
    response.status_code = 404
    return response
    
def handler500(request, exception = None):
    response = render(request = request, template_name = '500.html')
    response.status_code = 500
    return response

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

    page = request.GET.get('page')
    news = NewsLetter.objects.order_by('-date_published')
    home, aside, header, chatroom, profile, newsletter = None, None, None, None, None, None
    
    # Shared pages
    aside = get_aside_data()
    header = get_header_data(user_key = user_key, news = news)

    # Individual pages
    if page == 'home':
        home = get_home_data(user_key = user_key, news = news)    
    elif page == 'newsletter':        
        newsletter = get_newsletter_data(news = news)
    elif page == 'chatroom':        
        chatroom = get_chatroom_data(user_key = user_key)
    elif page == 'profile':
        profile = get_profile_data(user_key = user_key)    


    # Data for index.html
    data = {
        'profile': profile,                 # Data for profile.html
        'aside': aside,                     # Data for aside.html
        'home': home,                       # Data for home.html
        'header': header,                   # Data for header.html
        'chatroom': chatroom,               # Data for chatroom.html
        'newsletter': newsletter,           # Data for newsletter.html

        'page': page,
        'user_key': user_key,
        'title': page,
    }

    return render(request = request, context = data, template_name = 'dashboard/index.html')

# ------------------------------------------------------------------------ Profile ------------------------------------------------------------------------

@require_http_methods(['POST'])
def profile_update(request, user_key):

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

def get_user(user_key):
    return User.objects.get(user_key = user_key)


def get_site(user):
    return Site.objects.get(id = user.site_id)


def get_newsletter_data(news):

    newsletter = {
        'letters': news,
    }
    return newsletter


def get_aside_data():
    
    menu = Menu.objects.filter(category = 'Shared')
    aside = {
        'menu': menu,        
    }
    return aside


def get_header_data(user_key, news):

    user = get_user(user_key = user_key)   
    notifications = news.filter(date_published__gte = datetime.now() - timedelta(days = 7)) 

    header = {        
        'username': user.username,                
        'role': user.role,
        'notifications': notifications,
    }
    return header


def get_home_data(user_key, news):

    user = get_user(user_key = user_key)
    site = get_site(user = user)

    home = {
        'firstname': user.firstname,
        'lastname': user.lastname,
        'sitename': site.name,
        'role': user.role,
        'news': news,
    }
    return home


def get_chatroom_data(user_key):

    user = get_user(user_key = user_key)
    site = get_site(user = user)
    open_rooms = Room.objects.exclude(status = 'closed').order_by('-date_opened')       # Fetch open rooms
    assigned_rooms = open_rooms.filter(user_id__user_key = user_key)                    # Query assigned rooms

    chatroom = {
        'open_rooms': open_rooms,
        'assigned_rooms': assigned_rooms,
        'hall_key': site.public_key,
    }
    return chatroom


def get_profile_data(user_key):

    user = get_user(user_key = user_key)
    site = get_site(user = user)
    log = Log.objects.filter(user_id = user.id).latest('datetime')
    other_users = User.objects.filter(site_id = user.site_id).exclude(id = user.id)

    profile = {
        'firstname': user.firstname,
        'lastname': user.lastname,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'sitename': site.name,
        'country': user.country,
        'city': user.city,        
        'bio': user.bio,
        'rating': user.rating,
        'last_login': log.datetime,
        'activities': len(Room.objects.filter(user_id = user.id)),
        'other_users': other_users,        
        'form': ProfileForm(auto_id = True, instance = user),
    }
    return profile