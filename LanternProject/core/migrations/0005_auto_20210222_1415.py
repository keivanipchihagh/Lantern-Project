# Generated by Django 3.1.6 on 2021-02-22 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210222_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coreuser',
            name='image',
            field=models.ImageField(blank=True, default=None, help_text='Size < 1Mb', null=True, upload_to='./', verbose_name='Profile Picture'),
        ),
        migrations.AlterField(
            model_name='coreuser',
            name='password',
            field=models.CharField(max_length=30),
        ),
    ]
