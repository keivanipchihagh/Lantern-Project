# Generated by Django 3.1.6 on 2021-02-18 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CorePackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=300)),
                ('ip', models.CharField(blank=True, max_length=15, null=True)),
                ('datetime', models.DateTimeField()),
            ],
            options={
                'db_table': 'core_package',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CoreSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(max_length=64, unique=True)),
                ('status', models.CharField(max_length=6)),
                ('date_opened', models.DateTimeField()),
                ('date_closed', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'core_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CoreSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=50, unique=True)),
                ('private_key', models.CharField(max_length=512, unique=True)),
                ('public_key', models.CharField(max_length=512, unique=True)),
                ('date_joined', models.DateTimeField()),
                ('date_expires', models.DateTimeField()),
                ('service', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'core_site',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CoreUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('role', models.CharField(max_length=5)),
                ('status', models.CharField(max_length=7)),
                ('user_key', models.CharField(max_length=255, unique=True)),
                ('last_online', models.DateTimeField(blank=True, null=True)),
                ('date_joined', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'core_user',
                'managed': False,
            },
        ),
    ]