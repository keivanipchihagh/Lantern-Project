from django.db import models
from datetime import datetime, timedelta, timezone
from core.models import CoreUser


class DashboardMenu(models.Model):
    ''' Dashboard Menu model '''    

    # Name | Max Length: 20
    name = models.CharField(
        name = 'name',
        max_length = 20,
        unique = True,        
    )

    # Icon | Max Length: 20
    icon = models.CharField(
        name = 'icon',
        max_length = 20,
    )

    # Label | Max Length: 10
    label = models.CharField(
        name = 'label',
        max_length = 10,
        null = True,
    )

    # Category | Shared, Agent, Admin, Staff | Max Length: 6
    category = models.CharField(
        name = 'category',
        max_length = 6,
    )

    class Meta:
        managed = True          # Allow Create, Delete
        db_table = 'dashboard_menu'


class DashboardNewsLetter(models.Model):
    ''' Dashboard News Letter Model '''

    # Title | Max Length: 50
    title = models.CharField(
        name = 'title',
        max_length = 50,
    )

    # Type | Max Length: 30
    type = models.CharField(
        name = 'type',
        max_length = 30,
    )

    # DateTime
    date_published = models.DateTimeField(
        name = 'date_published',
        verbose_name = 'Published Date',
        default = datetime.now(timezone.utc),        
    )

    # Content | Max Length: 300
    content = models.TextField(
        name = 'content',
        max_length = 500,
    )

    # Tags | Max Length: 30
    tags = models.CharField(
        name = 'tags',
        max_length = 30,
    )

    # User Id  | Foreign Key (CoreUser.id)
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)

    def tags_as_list(self):
        return self.tags.split(',')

    def date_published_display(self):
        return (datetime.now(timezone.utc) - self.date_published).days

    class Meta:
        managed = True          # Allow Create, Delete
        db_table = 'dashboard_newsletter'