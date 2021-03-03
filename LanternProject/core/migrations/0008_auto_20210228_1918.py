# Generated by Django 3.1.6 on 2021-02-28 15:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210226_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corelog',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 28, 19, 18, 36, 253493)),
        ),
        migrations.AlterField(
            model_name='coreroom',
            name='date_opened',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 28, 19, 18, 36, 252439)),
        ),
        migrations.AlterField(
            model_name='coresite',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 28, 19, 18, 36, 253493)),
        ),
    ]
