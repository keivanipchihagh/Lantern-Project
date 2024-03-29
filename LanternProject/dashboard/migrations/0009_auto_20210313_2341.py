# Generated by Django 3.1.6 on 2021-03-13 20:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20210313_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='accept_text',
            field=models.CharField(default='OK', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='log',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 13, 23, 40, 57, 13994)),
        ),
        migrations.AlterField(
            model_name='room',
            name='date_opened',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 13, 23, 40, 57, 13994)),
        ),
        migrations.AlterField(
            model_name='site',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 13, 23, 40, 57, 13994)),
        ),
    ]
