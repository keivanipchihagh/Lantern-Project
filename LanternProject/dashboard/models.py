from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from datetime import datetime

class Menu(models.Model):
    ''' Menu model '''    

    # Name | Max Length: 20
    name = models.CharField(
        name = 'name',
        max_length = 20,
        unique = True,        
    )

    # Icon | Max Length: 20
    icon = models.CharField(
        name = 'icon',
        max_length = 20,
    )

    # Label | Max Length: 10
    label = models.CharField(
        name = 'label',
        max_length = 10,
        null = True,
    )

    # Category | Shared, Agent, Admin, Staff | Max Length: 6
    category = models.CharField(
        name = 'category',
        max_length = 6,
    )

    class Meta:
        managed = True          # Allow Create, Delete
        db_table = 'dashboard_menu'


class Notification(models.Model):
    ''' Notification Model '''

    # Title | Max Length: 50
    title = models.CharField(
        name = 'title',
        max_length = 30,
        help_text = 'Max length: 50',
    )

    # DateTime
    date_published = models.DateTimeField(
        name = 'date_published',
        verbose_name = 'Published Date',
    )

    # Content | Max Length: 500
    content = models.TextField(
        name = 'content',
        max_length = 500,
        help_text = 'Max Length: 500',
    )

    # Tag | Max Length: 30
    tag = models.CharField(
        name = 'tag',
        max_length = 30,
    )

    # Accept Text | Max Length: 30
    accept_text = models.CharField(
        name = 'accept_text',
        max_length = 30
    )

    # User Id  | Foreign Key (User.id)
    user = models.ForeignKey('User', models.DO_NOTHING)

    def tags_as_list(self):
        return self.tags.split(',')

    class Meta:
        managed = True          # Allow Create, Delete
        db_table = 'dashboard_notification'


class NotificationPanel(models.Model):

    # Notification Id  | Foreign Key (Notification.id)
    notification = models.ForeignKey('Notification', models.DO_NOTHING)

    # User Id  | Foreign Key (User.id)
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = True          # Allow Create, Delete
        db_table = 'dashboard_notification_panel'


class ReservedMessages(models.Model):
    ''' Reserved messages model '''

    # Title | Max Length: 30
    title = models.CharField(
        name = 'title',
        max_length = 30,
        help_text = 'Max Length: 30' 
    )

    # Tag | Max Length: 30
    tag = models.CharField(
        name = 'tag',
        max_length = 15,
        help_text = 'Max Length: 15',
        blank = True,
        default = 'general',
    )

    # Tag color | Max Length: 15
    COLOR_CHOICES = (
        ['INDIGO', 'indigo'],
        ['GREEN', 'green'],
        ['BLACK', 'black'],
        ['PURPLE', 'purple'],
        ['PINK', 'pink'],
        ['LIME', 'lime'],
        ['TEAL', 'teal'],
        ['CYAN', 'cyan'],
        ['BLUE', 'blue'],
    )
    color = models.CharField(
        name = 'color',
        max_length = 15,
        choices = COLOR_CHOICES,
        default = COLOR_CHOICES[0][0],
    )

    # Content | Max Length: 500
    content = models.TextField(
        name = 'content',
        max_length = 500,
        help_text = 'Max Length: 500',
    )

    # Starred | Boolean
    starred = models.BooleanField(
        name = 'starred',
        default = 0,
        null = True,
        blank = True,
    )

    # Date_Modified | Datetime
    date_modified = models.DateTimeField(
        name = 'date_modified',
        verbose_name = 'Modified Date'
    )

    # User Id  | Foreign Key (User.id)
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = True          # Allow Create, Delete
        db_table = 'dashboard_reservedmessages'


class Message(models.Model):
    ''' Message model '''

    # Content | Max Length: 300
    content = models.CharField(
        max_length = 300,
        name = 'content',
        )
    
    # Sender | Max Length: 6 | {1: client, 0: server}
    client = models.BooleanField(
        name = 'client',
        default = True,
    )

    # DateTime | DateTime
    datetime = models.DateTimeField(
        name = 'datetime',
    )

    # Room Id | Foreign Key (Room.id)
    room = models.ForeignKey('Room', models.DO_NOTHING)

    def as_dict(self):
        return {
            'content': self.content,
            'datetime': self.datetime.strftime("%I:%M %p"),     # Ex. 12:34 AM
            'sender': self.sender,
            'room_id': self.room.id,
        }

    class Meta:
        managed = True          # Allow Create, Delete
        db_table = 'dashboard_message'


class Room(models.Model):
    ''' Room model '''

    # Room Key | Max Length: 64
    room_key = models.CharField(
        unique = True,
        name = 'room_key',
        max_length = 64,
        )

    # Status | Max Length: 6 | open, closed
    status = models.CharField(
        max_length = 8,
        name = 'status',
        validators = [RegexValidator('^{open|closed}$', message = "Status Unknonw")],
        default = 'open',
        )
    
    # IP Address | Max Length: 15
    ip = models.CharField(
        max_length = 15,
        name = 'ip',
        blank = True,
        null = True,
        )

    # Date Opened | DateTime
    date_opened = models.DateTimeField(
        name = 'date_opened',
        default = datetime.now(),
    )

    # Date Closed | DateTime
    date_closed = models.DateTimeField(
        blank = True,
        name = 'date_closed',
        null = True,
        default = None,
        )

    # Topic | Max Length: 30
    topic = models.CharField(
        name = 'topic',
        max_length = 30,
    )

    # User Id  | Foreign Key (User.id)
    user = models.ForeignKey('User', models.DO_NOTHING)

    # Site Id | Foreign Key (Site.id)
    site = models.ForeignKey('Site', models.DO_NOTHING)

    class Meta:
        managed = True          # Allow Create, Delete
        db_table = 'dashboard_room'


class Site(models.Model):
    ''' Site model '''

    # Host | Max Length: 50
    host = models.CharField(
        max_length = 50,
        name = 'host',
        unique = True,
        )

    # URL | Max Length: 50
    url = models.CharField(
        unique = True,
        name = 'url',
        max_length = 50,        
        )

    # Private Key | Max Length: 128
    private_key = models.CharField(
        unique = True,
        name = 'private_key',
        max_length = 128,
        )

    # Public Key | Max Length: 128
    public_key = models.CharField(
        unique = True,
        name = 'public_key',
        max_length = 128
        )

    # Date Joined | DateTime
    date_joined = models.DateTimeField(
        name = 'date_joined',
        default = datetime.now(),
    )

    # Expire Date | DateTime
    date_expires = models.DateTimeField(
        blank = True,
        name = 'date_expires',
        null = True,
    )

    # LiveChat Service | Boolean
    livechat_service = models.BooleanField(
        name = 'livechat_service',
        default = True,
    )

    # Ticket Service | Boolean
    ticket_service = models.BooleanField(
        name = 'ticket_service',
        default = True,
    )

    # VirtualAgent | Boolean
    virtualagent_service = models.BooleanField(
        name = 'virtualagent_service',
        default = False
    )

    class Meta:
        managed = True          # Allow Create, Delete
        db_table = 'dashboard_site'


class Log(models.Model):
    ''' Log model '''

    # Title | Max Length: 30
    title = models.CharField(
        name = 'title',
        max_length = 30,
    )    

    # Datetime | Datetime
    datetime = models.DateTimeField(
        name = 'datetime',
        default = datetime.now(),
    )

    # User Id  | Foreign Key (User.id)
    user = models.ForeignKey('User', models.DO_NOTHING)

    # Site Id | Foreign Key (Site.id)
    site = models.ForeignKey('Site', models.DO_NOTHING)

    class Meta:
        managed = True          # Allow Create, Delete
        db_table = 'dashboard_log'


class User(AbstractUser):
    ''' User model '''

    # Email | Override
    email = models.EmailField(
        name = 'email',
        unique = True,
        max_length = 150,
        verbose_name = 'Email Address',
    )

    username = models.CharField(
        name = 'username',
        max_length = 50,
        validators = [RegexValidator('^[A-Za-z ]+$', message = "Letters allowed only!")],
        unique = True,        
    )

    # Phone Number | Max Length: 12
    phone_number = models.CharField(
        max_length = 11,
        name = 'phone_number',        
        validators = [RegexValidator('^[0-9]+$', message = "Numbers allowed only!")],
        help_text = 'Format: XXXX XXX XXXX',
        verbose_name = 'Phone Number'
    )

    # Title | Max Length: 30 | ie. Sales Manager
    title = models.CharField(
        name = 'title',
        max_length = 30,
        null = True,
        validators = [RegexValidator('^[A-Za-z ]+$', message = "Letters allowed only!")]
    )

    # Rating | Float
    rating = models.FloatField(
        blank = True,
        name = 'rating',
        null = True,        
    )

    # Site Id | Foreign Key (Site.id)
    site = models.ForeignKey('Site', models.DO_NOTHING, verbose_name = 'Assigned Site')

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    class Meta:
        managed = True          # Allow Create, Delete
        db_table = 'dashboard_user'
