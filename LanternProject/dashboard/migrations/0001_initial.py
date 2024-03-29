# Generated by Django 3.1.6 on 2021-03-10 14:27

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phonenumber', models.CharField(help_text='Format: XXXX XXX XXXX', max_length=11, validators=[django.core.validators.RegexValidator('^[0-9]+$', message='Numbers allowed only!')], verbose_name='Phone Number')),
                ('title', models.CharField(max_length=30, null=True, validators=[django.core.validators.RegexValidator('^[A-Za-z ]+$', message='Letters allowed only!')])),
                ('rating', models.FloatField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'db_table': 'dashboard_user',
                'managed': True,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('icon', models.CharField(max_length=20)),
                ('label', models.CharField(max_length=10, null=True)),
                ('category', models.CharField(max_length=6)),
            ],
            options={
                'db_table': 'dashboard_menu',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=50, unique=True)),
                ('url', models.CharField(max_length=50, unique=True)),
                ('private_key', models.CharField(max_length=128, unique=True)),
                ('public_key', models.CharField(max_length=128, unique=True)),
                ('date_joined', models.DateTimeField(default=datetime.datetime(2021, 3, 10, 17, 57, 14, 910347))),
                ('date_expires', models.DateTimeField(blank=True, null=True)),
                ('livechat_service', models.BooleanField(default=True)),
                ('ticket_service', models.BooleanField(default=True)),
                ('virtualagent_service', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'dashboard_site',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_key', models.CharField(max_length=64, unique=True)),
                ('status', models.CharField(default='open', max_length=8, validators=[django.core.validators.RegexValidator('^{open|closed}$', message='Status Unknonw')])),
                ('ip', models.CharField(blank=True, max_length=15, null=True)),
                ('date_opened', models.DateTimeField(default=datetime.datetime(2021, 3, 10, 17, 57, 14, 910347))),
                ('date_closed', models.DateTimeField(blank=True, default=None, null=True)),
                ('topic', models.CharField(max_length=30)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.site')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'dashboard_room',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ReservedMessages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Max Length: 30', max_length=30)),
                ('tag', models.CharField(blank=True, default='general', help_text='Max Length: 15', max_length=15)),
                ('color', models.CharField(choices=[['INDIGO', 'indigo'], ['GREEN', 'green'], ['BLACK', 'black'], ['PURPLE', 'purple'], ['PINK', 'pink'], ['LIME', 'lime'], ['TEAL', 'teal'], ['CYAN', 'cyan'], ['BLUE', 'blue']], default='INDIGO', max_length=15)),
                ('content', models.TextField(help_text='Max Length: 500', max_length=500)),
                ('starred', models.BooleanField(blank=True, default=0, null=True)),
                ('date_modified', models.DateTimeField(verbose_name='Modified Date')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'dashboard_reservedmessages',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='NewsLetter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Max length: 50', max_length=50)),
                ('type', models.CharField(choices=[('general', 'general'), ('maintenance', 'maintenance'), ('update', 'update')], default='general', max_length=30)),
                ('date_published', models.DateTimeField(verbose_name='Published Date')),
                ('content', models.TextField(help_text='Max Length: 500', max_length=500)),
                ('tags', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'dashboard_newsletter',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=300)),
                ('client', models.BooleanField(default=True)),
                ('datetime', models.DateTimeField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.room')),
            ],
            options={
                'db_table': 'dashboard_message',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('datetime', models.DateTimeField(default=datetime.datetime(2021, 3, 10, 17, 57, 14, 911349))),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.site')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'dashboard_log',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='user',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.site', verbose_name='Assigned Site'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
