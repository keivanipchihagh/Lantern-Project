from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime


class CoreMessage(models.Model):
    ''' Core Message model '''

    # Content | Max Length: 300
    content = models.CharField(
        max_length = 300,
        name = 'content',
        )

    # IP Address | Max Length: 15
    ip = models.CharField(
        max_length = 15,
        name = 'ip',
        blank = True,
        null = True,
        )
    
    # Sender | Max Length: 6 | client, agent
    sender = models.CharField(
        max_length = 6,
        name = 'sender',
        )

    # DateTime | DateTime
    datetime = models.DateTimeField(
        name = 'datetime',
    )

    # Session Id | Foreign Key (CoreSession.id)
    session = models.ForeignKey('CoreSession', models.DO_NOTHING)

    def as_dict(self):
        return {
            'content': self.content,
            'datetime': self.datetime.strftime("%I:%M %p"),     # Ex. 12:34 AM
            'sender': self.sender,
            'session_id': self.session.id,
            'starred': self.session.starred,
        }

    class Meta:
        managed = True          # Allow Create, Delete
        db_table = 'core_message'


class CoreSession(models.Model):
    ''' Core Session model '''

    # Session Key | Max Length: 64
    session_key = models.CharField(
        unique = True,
        name = 'session_key',
        max_length = 64,
        )

    # Status | Max Length: 6 | open, closed
    status = models.CharField(
        max_length = 6,
        name = 'status',
        validators = [RegexValidator('^{open|closed}$', message = "Status Unknonw")],
        default = 'open',
        )

    # Starred | Boolean
    starred = models.BooleanField(
        default = False,
        name = 'starred',        
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

    # User Id  | Foreign Key (CoreUser.id)
    user = models.ForeignKey('CoreUser', models.DO_NOTHING)

    # Site Id | Foreign Key (CoreSite.id)
    site = models.ForeignKey('CoreSite', models.DO_NOTHING)

    class Meta:
        managed = True          # Allow Create, Delete
        db_table = 'core_session'


class CoreSite(models.Model):
    ''' Core Site model '''

    # Name | Max Length: 50
    name = models.CharField(
        max_length = 50,
        name = 'name',
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

    # Service | Boolean
    service = models.BooleanField(
        name = 'service',
        default = True,
        )

    class Meta:
        managed = True          # Allow Create, Delete
        db_table = 'core_site'


class CoreUser(models.Model):
    ''' Core User model '''

    # Firstname | Max Length: 30
    firstname = models.CharField(
        max_length = 30,
        name = 'firstname',
        help_text = 'Max Length: 30',
        validators = [RegexValidator('^[A-Za-z ]+$', message = "Letters allowed only!")]
        )

    # Lastname | Max Length: 30
    lastname = models.CharField(
        max_length = 30,
        name = 'lastname',
        help_text = 'Max Length: 30',
        validators = [RegexValidator('^[A-Za-z ]+$', message = "Letters allowed only!")]
        )

    # Email Address | Max Length: 50
    email = models.EmailField(
        unique = True,
        max_length = 50,
        name = 'email',
        help_text = 'Max length: 30',
        verbose_name = 'Email Address'
        )

    # Username | Max Length: 30
    username = models.CharField(
        unique = True,
        max_length = 30,
        name = 'username',
        help_text = 'Max length: 30',
        )

    # Password | Max Length: 30
    password = models.CharField(
        max_length = 30,
        name = 'password',
        )

    # Phone Number | Max Length: 12
    phonenumber = models.CharField(
        max_length = 12,
        name = 'phonenumber',        
        validators = [RegexValidator('^[0-9]+$', message = "Numbers allowed only!")],
        help_text = 'Format: XXXX XXX XXX',
        verbose_name = 'Phone Number'
        )

    # Role | Max Length: 5
    role = models.CharField(
        max_length = 5,
        name = 'role',
        validators = [RegexValidator('{staff|admin|agent}', message = 'Role Unknown')],
        )

    # Country | Max Length: 30
    country = models.CharField(
        max_length = 30,
        name = 'country',
        blank = True,
        null = True,
        help_text = 'Max length: 30',
        validators = [RegexValidator('^[A-Za-z ]+$', message = "Letters allowed only!")],
        )

    # City | Max Length: 30
    city = models.CharField(
        max_length = 30,
        name = 'city',
        blank = True,
        null = True,
        help_text = 'Max length: 30',
        validators = [RegexValidator('^[A-Za-z ]+$', message = "Letters allowed only!")],
        )

    # Bio | Max Length: 75
    bio = models.CharField(
        max_length = 75,
        name = 'bio',
        blank = True,
        null = True,
        default = 'Howdy!',
        help_text = 'Max length: 30',
        )

    # Rating | Float
    rating = models.FloatField(
        blank = True,
        name = 'rating',
        null = True,        
        )

    # User Key | Max Length: 128
    user_key = models.CharField(
        unique = True,
        name = 'user_key',
        max_length = 128,
        )

    # Profile Image | File (Image)
    image = models.ImageField(
        upload_to = './',
        name = 'image',
        null = True,
        blank = True,
        default = None,
        help_text = 'Size < 1Mb',
        verbose_name = 'Profile Picture'
        )

    # Site Id | Foreign Key (CoreSite.id)
    site = models.ForeignKey(CoreSite, models.DO_NOTHING, verbose_name = 'Assigned Site')

    class Meta:
        managed = True          # Allow Create, Delete
        db_table = 'core_user'


class CoreLog(models.Model):
    ''' Core Log model '''

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

    # User Id  | Foreign Key (CoreUser.id)
    user = models.ForeignKey('CoreUser', models.DO_NOTHING)

    class Meta:
        managed = True          # Allow Create, Delete
        db_table = 'core_log'
        