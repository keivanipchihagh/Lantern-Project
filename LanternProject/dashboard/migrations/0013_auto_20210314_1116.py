# Generated by Django 3.1.6 on 2021-03-14 07:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_auto_20210314_0109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='ip',
        ),
        migrations.AlterField(
            model_name='log',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 14, 11, 16, 47, 770373)),
        ),
        migrations.AlterField(
            model_name='room',
            name='date_opened',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 14, 11, 16, 47, 769374)),
        ),
        migrations.AlterField(
            model_name='site',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 14, 11, 16, 47, 770373)),
        ),
    ]
