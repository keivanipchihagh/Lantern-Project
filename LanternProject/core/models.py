# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CorePackage(models.Model):
    message = models.CharField(max_length=300)
    ip = models.CharField(max_length=15, blank=True, null=True)
    datetime = models.DateTimeField()
    session = models.ForeignKey('CoreSession', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'core_package'


class CoreSession(models.Model):
    session_key = models.CharField(unique=True, max_length=64)
    status = models.CharField(max_length=6)
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
    status = models.CharField(max_length=7)
    user_key = models.CharField(unique=True, max_length=255)
    last_online = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)
    site = models.ForeignKey(CoreSite, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'core_user'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
