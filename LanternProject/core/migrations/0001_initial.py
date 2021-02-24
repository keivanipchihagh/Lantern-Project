# Generated by Django 3.1.6 on 2021-02-24 05:33

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoreSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('url', models.CharField(max_length=50, unique=True)),
                ('private_key', models.CharField(max_length=128, unique=True)),
                ('public_key', models.CharField(max_length=128, unique=True)),
                ('date_joined', models.DateTimeField(default=datetime.datetime(2021, 2, 24, 9, 3, 47, 905233))),
                ('date_expires', models.DateTimeField(blank=True, null=True)),
                ('service', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'core_site',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CoreUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(help_text='Max Length: 30', max_length=30, validators=[django.core.validators.RegexValidator('^[A-Za-z ]+$', message='Letters allowed only!')])),
                ('lastname', models.CharField(help_text='Max Length: 30', max_length=30, validators=[django.core.validators.RegexValidator('^[A-Za-z ]+$', message='Letters allowed only!')])),
                ('email', models.EmailField(help_text='Max length: 30', max_length=50, unique=True, verbose_name='Email Address')),
                ('username', models.CharField(help_text='Max length: 30', max_length=30, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('phonenumber', models.CharField(help_text='Format: XXXX XXX XXX', max_length=12, validators=[django.core.validators.RegexValidator('^[0-9]+$', message='Numbers allowed only!')], verbose_name='Phone Number')),
                ('role', models.CharField(max_length=5, validators=[django.core.validators.RegexValidator('{staff|admin|agent}', message='Role Unknown')])),
                ('country', models.CharField(blank=True, help_text='Max length: 30', max_length=30, null=True, validators=[django.core.validators.RegexValidator('^[A-Za-z ]+$', message='Letters allowed only!')])),
                ('city', models.CharField(blank=True, help_text='Max length: 30', max_length=30, null=True, validators=[django.core.validators.RegexValidator('^[A-Za-z ]+$', message='Letters allowed only!')])),
                ('bio', models.CharField(blank=True, default='Howdy!', help_text='Max length: 30', max_length=75, null=True)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('user_key', models.CharField(max_length=128, unique=True)),
                ('image', models.ImageField(blank=True, default=None, help_text='Size < 1Mb', null=True, upload_to='./', verbose_name='Profile Picture')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.coresite', verbose_name='Assigned Site')),
            ],
            options={
                'db_table': 'core_user',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CoreRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_key', models.CharField(max_length=64, unique=True)),
                ('status', models.CharField(default='open', max_length=6, validators=[django.core.validators.RegexValidator('^{open|closed}$', message='Status Unknonw')])),
                ('starred', models.BooleanField(default=False)),
                ('date_opened', models.DateTimeField(default=datetime.datetime(2021, 2, 24, 9, 3, 47, 905233))),
                ('date_closed', models.DateTimeField(blank=True, default=None, null=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.coresite')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.coreuser')),
            ],
            options={
                'db_table': 'core_room',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CoreMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=300)),
                ('ip', models.CharField(blank=True, max_length=15, null=True)),
                ('sender', models.CharField(max_length=6)),
                ('datetime', models.DateTimeField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.coreroom')),
            ],
            options={
                'db_table': 'core_message',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CoreLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('datetime', models.DateTimeField(default=datetime.datetime(2021, 2, 24, 9, 3, 47, 906232))),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.coresite')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.coreuser')),
            ],
            options={
                'db_table': 'core_log',
                'managed': True,
            },
        ),
    ]
