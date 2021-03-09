# Generated by Django 3.1.6 on 2021-03-05 20:54

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20210305_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corelog',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 6, 0, 24, 47, 863582)),
        ),
        migrations.AlterField(
            model_name='coreroom',
            name='date_opened',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 6, 0, 24, 47, 861581)),
        ),
        migrations.AlterField(
            model_name='coresite',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 6, 0, 24, 47, 862586)),
        ),
        migrations.CreateModel(
            name='CoreCustomization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Hello There!', max_length=20)),
                ('placeholder', models.CharField(default='Ask us anything, or share your feedback.', max_length=30)),
                ('livechat_title', models.CharField(default='Start a conversation', max_length=20)),
                ('livechat_placeholder_online', models.CharField(default='We are ready to assist', max_length=30)),
                ('livechat_placeholder_offline', models.CharField(default='We are not currently online.', max_length=30)),
                ('ticket_title', models.CharField(default='Leave a Ticket', max_length=20)),
                ('ticket_placeholder_online', models.CharField(default='We will contact you by email', max_length=30)),
                ('virtualagent_title', models.CharField(default='Virtual Agent', max_length=20)),
                ('virtualagent_placeholder_online', models.CharField(default='Try our AI powered agent.', max_length=30)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.coresite')),
            ],
            options={
                'db_table': 'core_customization',
                'managed': True,
            },
        ),
    ]