# Generated by Django 3.1.6 on 2021-03-10 15:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20210310_1859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email address',
        ),
        migrations.AlterField(
            model_name='log',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 10, 18, 59, 54, 326308)),
        ),
        migrations.AlterField(
            model_name='room',
            name='date_opened',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 10, 18, 59, 54, 325308)),
        ),
        migrations.AlterField(
            model_name='site',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 10, 18, 59, 54, 325308)),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=150, unique=True),
        ),
    ]