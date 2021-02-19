# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CoreMessage(models.Model):
    content = models.CharField(max_length=300)
    ip = models.CharField(max_length=15, blank=True, null=True)
    sender = models.CharField(max_length=6, blank=True, null=True)
    datetime = models.DateTimeField()
    session = models.ForeignKey('CoreSession', models.DO_NOTHING)

    def as_dict(self):
        return {
            'content': self.content,
            'datetime': self.datetime.strftime("%I:%M %p"),
            'sender': self.sender,
            'session_id': self.session.id,
            'starred': self.session.starred,
        }

    class Meta:
        managed = False
        db_table = 'core_message'


class CoreSession(models.Model):
    session_key = models.CharField(unique=True, max_length=64)
    status = models.CharField(max_length=6)
    starred = models.IntegerField()
    date_opened = models.DateTimeField()
    date_closed = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('CoreUser', models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey('CoreSite', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'core_session'


class CoreSite(models.Model):
    url = models.CharField(unique=True, max_length=50)
    private_key = models.CharField(unique=True, max_length=512)
    public_key = models.CharField(unique=True, max_length=512)
    date_joined = models.DateTimeField()
    date_expires = models.DateTimeField()
    service = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_site'


class CoreUser(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.CharField(unique=True, max_length=50)
    username = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=30)
    role = models.CharField(max_length=5)
    location = models.CharField(max_length=30, blank=True, null=True)
    bio = models.CharField(max_length=75, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    user_key = models.CharField(unique=True, max_length=255)
    last_online = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)
    site = models.ForeignKey(CoreSite, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'core_user'