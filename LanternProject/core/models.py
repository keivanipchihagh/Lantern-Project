from django.db import models


class CoreMessage(models.Model):
    content = models.CharField(max_length = 300)                                                # Content           | Max Length: 300
    ip = models.CharField(max_length = 15, blank = True, null = True)                           # IP Address        | Max Length: 15
    sender = models.CharField(max_length = 6, blank = True, null = True)                        # Sender            | Max Length: 6                 | client, agent
    datetime = models.DateTimeField()                                                           # DateTime          | DateTime
    session = models.ForeignKey('CoreSession', models.DO_NOTHING)                               # Session Id        | Foreign Key (CoreSession.id)

    # Formatter
    def as_dict(self):
        return {
            'content': self.content,
            'datetime': self.datetime.strftime("%I:%M %p"),     # Ex. 12:34 AM
            'sender': self.sender,
            'session_id': self.session.id,
            'starred': self.session.starred,
        }

    class Meta:
        managed = True
        db_table = 'core_message'


class CoreSession(models.Model):
    session_key = models.CharField(unique = True, max_length = 64)                              # Session Key       | Max Length: 64
    status = models.CharField(max_length = 6)                                                   # Status            | Max Length: 6                 | open, closed
    starred = models.BooleanField()                                                             # Starred           | Boolean
    date_opened = models.DateTimeField()                                                        # Date Opened       | DateTime
    date_closed = models.DateTimeField(blank = True, null = True)                               # Date Closed       | DateTime
    user = models.ForeignKey('CoreUser', models.DO_NOTHING, blank = True, null = True)          # User Id           | Foreign Key (CoreUser.id)
    site = models.ForeignKey('CoreSite', models.DO_NOTHING)                                     # Site Id           | Foreign Key (CoreSite.id)

    class Meta:
        managed = True
        db_table = 'core_session'


class CoreSite(models.Model):
    name = models.CharField(max_length = 50, blank = True, null = True)                         # Name              | Max Length: 50
    url = models.CharField(unique = True, max_length = 50)                                      # URL               | Max Length: 50
    private_key = models.CharField(unique = True, max_length = 128)                             # Private Key       | Max Length: 128
    public_key = models.CharField(unique = True, max_length = 128)                              # Public Key        | Max Length: 128
    date_joined = models.DateTimeField()                                                        # Date Joined       | DateTime
    date_expires = models.DateTimeField()                                                       # Expire Date       | DateTime
    service = models.BooleanField(blank = True, null = True)                                    # Service           | Boolean

    class Meta:
        managed = True
        db_table = 'core_site'


class CoreUser(models.Model):
    firstname = models.CharField(max_length = 30)                                               # Firstname         | Max Length: 30
    lastname = models.CharField(max_length = 30)                                                # Lastname          | Max Length: 30
    email = models.EmailField(unique = True, max_length = 50)                                   # Email Address     | Max Length: 50
    username = models.CharField(unique = True, max_length = 30)                                 # Username          | Max Length: 30
    password = models.CharField(max_length = 30)                                                # Password          | Max Length: 30
    phonenumber = models.CharField(max_length = 12)                                             # Phone Number      | Max Length: 12
    role = models.CharField(max_length = 5)                                                     # Role              | Max Length: 5
    country = models.CharField(max_length = 30, blank = True, null = True)                      # Country           | Max Length: 30
    city = models.CharField(max_length = 30, blank = True, null = True)                         # City              | Max Length: 30
    bio = models.CharField(max_length = 75, blank = True, null = True)                          # Bio               | Max Length: 75
    rating = models.FloatField(blank = True, null = True)                                       # Rating            | Float
    user_key = models.CharField(unique = True, max_length = 128)                                # User Key          | Max Length: 128
    last_login = models.DateTimeField(blank = True, null = True)                                # Last Login        | DateTime
    date_joined = models.DateTimeField(blank = True, null = True)                               # Date Joined       | DateTime
    image = models.FileField(upload_to = 'A/', null = True)                                     # Profile Image     | File (Image)
    site = models.ForeignKey(CoreSite, models.DO_NOTHING)                                       # Site Id           | Foreign Key (CoreSite.id)

    class Meta:
        managed = True
        db_table = 'core_user'