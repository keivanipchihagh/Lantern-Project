# Generated by Django 3.1.6 on 2021-03-13 19:10

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20210313_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 13, 22, 40, 55, 590534)),
        ),
        migrations.AlterField(
            model_name='room',
            name='date_opened',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 13, 22, 40, 55, 589534)),
        ),
        migrations.AlterField(
            model_name='site',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 13, 22, 40, 55, 590534)),
        ),
        migrations.CreateModel(
            name='NotificationPanel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.notification')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'dashboard_notification_panel',
                'managed': True,
            },
        ),
    ]
