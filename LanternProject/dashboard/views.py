from django.http.response import  HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from .models import Menu, NewsLetter, ReservedMessages, Room, User, Message, Site, Log
import json
from .forms import ProfileForm, LoginForm, ReservedMessagesForm
from django.views.decorators.http import require_http_methods   # Request restrictions
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required


# ------------------------------------------------------------------------ Errors -------------------------------------------------------------------------

def handler404(request, exception = None):
    response = render(request = request, template_name = '404.html')
    response.status_code = 404
    return response
    
def handler500(request, exception = None):
    response = render(request = request, template_name = '500.html')
    response.status_code = 500
    return response

# -------------------------------------------------------------------- Authentication -------------------------------------------------------------------

@require_http_methods(['GET'])
def logout(request):
    auth_logout(request)


@require_http_methods(['GET', 'POST'])
def login(request):

    if request.method == 'GET':
        return render(request = request, context = {'form': LoginForm(auto_id = True, initial = {'email': '', 'password': ''})}, template_name = 'dashboard/login.html')
    else:
        form = LoginForm(request.POST)  # Apply validation rules

        if form.is_valid():

            # Get user if exists                
            user = authenticate(email = form.cleaned_data['email'], password = form.cleaned_data['password'])
                
            # Invalid credentials
            if user is None:
                return render(request = request, context = {'form': LoginForm(auto_id = True, initial = {'email': form.cleaned_data['email'], 'password': ''}), 'message': 'Invalid Email/Password'}, template_name = 'dashboard/login.html')

            # Session            
            if form.cleaned_data['remember_me']:
                request.session.set_expiry(24 * 60 * 60)    # 1 Day
            else:
                request.session.set_expiry(0)               # Logout on browser close

            auth_login(request, user)   # Authenticate

            # Cookie & remember_me
            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(0)

            # Log
            Log(title = 'Sign In', user_id = user.id, site_id = user.site_id).save()                

            return HttpResponseRedirect('v1/user/' + user.username)
        else:
            return HttpResponseForbidden(form.errors.values())

# ------------------------------------------------------------------------ Index ------------------------------------------------------------------------

@login_required(login_url = 'login')
@require_http_methods(['GET'])
def dashboard(request, username):

    page = request.GET.get('page')
    news = NewsLetter.objects.order_by('-date_published')
    home, aside, header, chatroom, profile, newsletter, reservedmessages = None, None, None, None, None, None, None
    
    # Shared pages
    aside = get_aside_data()
    header = get_header_data(username = username, news = news)

    # Set Cookies(Session: username & expire time)
    # return HttpResponse(request.session['username'])
    # request.session['username'] = username
    # request.session.set_expiry(60)

    # Individual pages
    if page == 'home':
        home = get_home_data(username = username, news = news)
        reservedmessages = get_reservedmessages_data(username = username)
    elif page == 'newsletter':        
        newsletter = get_newsletter_data(news = news)
    elif page == 'chatroom':        
        chatroom = get_chatroom_data(username = username)
        reservedmessages = get_reservedmessages_data(username = username)
    elif page == 'profile':
        profile = get_profile_data(username = username)
    elif page == 'reserved messages':
        reservedmessages = get_reservedmessages_data(username = username)


    # Data for index.html
    data = {
        'profile': profile,                     # Data for profile.html
        'aside': aside,                         # Data for aside.html
        'home': home,                           # Data for home.html
        'header': header,                       # Data for header.html
        'chatroom': chatroom,                   # Data for chatroom.html
        'newsletter': newsletter,               # Data for newsletter.html
        'reservedmessages': reservedmessages,   # Data for reservedmessages.html

        'page': page,
        'username': username,
        'title': page,
    }

    return render(request = request, context = data, template_name = 'dashboard/index.html')

# ------------------------------------------------------------------------ Profile ------------------------------------------------------------------------

@login_required(login_url = 'login')
@require_http_methods(['POST'])
def profile_update(request, username):

    form = ProfileForm(request.POST, request.FILES)

    if form.is_valid():
        User.objects.filter(username = username).update(
            first_name = form.cleaned_data.get('first_name'),
            last_name = form.cleaned_data.get('last_name'),
            phone_number = form.cleaned_data.get('phone_number'),
            country = form.cleaned_data.get('country'),
            city = form.cleaned_data.get('city'),
            bio = form.cleaned_data.get('bio'),
        )

        return HttpResponse('Updated, Reloading...')
    else:
        return HttpResponse(form.errors.as_text())  # Validation failed

# -------------------------------------------------------------------- Reserved Messages --------------------------------------------------------------------

@login_required(login_url = 'login')
@require_http_methods(['POST'])
def reversedmessages_modify(request, username):

    id = request.POST.get('id')
    title = request.POST.get('title')
    tag = request.POST.get('tag')
    color = request.POST.get('color').lower()
    starred = request.POST.get('starred')
    content = request.POST.get('content')

    user = get_user(username = username)

    if request.POST.get('action') == 'DELETE':
        reservedmessage = ReservedMessages.objects.get(id = id, user_id = user.id).delete()
    elif request.POST.get('action') == 'UPDATE':
        reservedmessage = ReservedMessages.objects.filter(id = id, user_id = user.id).update(
            title = title,
            tag = tag,
            color = color,
            starred = (starred == 'true'),
            content = content,
        )
    elif request.POST.get('action') == 'INSERT':
        ReservedMessages(
            title = title,
            tag = tag,
            color = color,
            starred = (starred == 'true'),
            content = content,
            user_id = user.id,
            date_modified = datetime.now(),
        ).save()

    return HttpResponse('')


# ------------------------------------------------------------------------ Chatroom ------------------------------------------------------------------------

@login_required(login_url = 'login')
def chatroom_assign_room(request, username):
    ''' Return the earliest created room key and it's messages assigned to the site that the agent belogns '''

    user = User.objects.get(username = username)
    assigned_room = Room.objects.filter(status = 'open', user_id = user.id).order_by('date_opened')[0]
    # assigned_room.status = 'assigned'
    # assigned_room.save()

    messages = Message.objects.filter(room_id = assigned_room.id)

    # Format messages
    dictionaries = [str(obj.as_dict()) for obj in messages]

    response = {
        'messages': dictionaries,
        'room_key': assigned_room.room_key
    }

    # Return serialized response
    return HttpResponse(json.dumps(response), content_type = 'application/json')


def chatroom_close_room(request):

    # Get request data
    room_key, username = request.GET['room_key'], request.GET['username']

    # Verification & update
    user = User.objects.get(username = username)
    room = Room.objects.get(room_key = room_key, user_id = user.id)
    room.status = 'closed'
    room.save()

    # Remove messages for the room
    Message.objects.filter(room_id = room.id).delete()

    # Return empty response
    return HttpResponse('')

# ------------------------------------------------------------------------ Methods ------------------------------------------------------------------------

def get_user(username):
    return User.objects.get(username = username)


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


def get_header_data(username, news):

    user = get_user(username = username)   
    notifications = news.filter(date_published__gte = datetime.now() - timedelta(days = 7)) 

    header = {        
        'username': user.username,                
        # 'role': user.role,
        'notifications': notifications,
    }
    return header


def get_home_data(username, news):

    user = get_user(username = username)
    site = get_site(user = user)

    home = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'hostname': site.host,
        # 'role': user.role,
        'news': news,
    }
    return home


def get_chatroom_data(username):

    user = get_user(username = username)
    site = get_site(user = user)
    open_rooms = Room.objects.exclude(status = 'closed').order_by('-date_opened')       # Fetch open rooms
    assigned_rooms = open_rooms.filter(user_id__username = username)                    # Query assigned rooms

    chatroom = {
        'open_rooms': open_rooms,
        'assigned_rooms': assigned_rooms,
        'hall_key': site.public_key,
    }
    return chatroom


def get_profile_data(username):

    user = get_user(username = username)
    site = get_site(user = user)
    log = Log.objects.filter(user_id = user.id).latest('datetime')
    other_users = User.objects.filter(site_id = user.site_id).exclude(id = user.id)

    profile = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        # 'role': user.role,
        'hostname': site.host,
        'rating': user.rating,
        'last_login': log.datetime,
        'assigned_rooms_count': len(Room.objects.filter(user_id = user.id)),
        'other_users': other_users,        
        'form': ProfileForm(auto_id = True, instance = user),
    }
    return profile


def get_reservedmessages_data(username):

    user = get_user(username = username)
    messages = ReservedMessages.objects.filter(user_id = user.id).order_by('tag', 'title')
    tags = messages.order_by().values('tag', 'color').distinct()

    reservedmessages = {
        'messages': messages,
        'tags': tags,
        'form': ReservedMessagesForm(auto_id = True),
    }

    return reservedmessages