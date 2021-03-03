from django.db import models
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
        help_text = 'Max length: 50',
    )

    # Type | Max Length: 30
    type = models.CharField(
        name = 'type',
        max_length = 30,
        choices = [
            ('general', 'general'),
            ('maintenance', 'maintenance'),
            ('update', 'update'),
        ],
        default = 'general',
    )

    # DateTime
    date_published = models.DateTimeField(
        name = 'date_published',
        verbose_name = 'Published Date',
    )

    # Content | Max Length: 500
    content = models.TextField(
        name = 'content',
        max_length = 500,
        help_text = 'Max Length: 500',
    )

    # Tags | Max Length: 30 | announcement, user.role, update, maintenance, automated
    tags = models.CharField(
        name = 'tags',
        max_length = 100,
    )

    # User Id  | Foreign Key (CoreUser.id)
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)

    def tags_as_list(self):
        return self.tags.split(',')

    class Meta:
        managed = True          # Allow Create, Delete
        db_table = 'dashboard_newsletter'


class DashboardReservedMessages(models.Model):
    ''' Dashboard Reserved messages model '''

    # Title | Max Length: 30
    title = models.CharField(
        name = 'title',
        max_length = 30,
        help_text = 'Max Length: 30' 
    )

    # Tag | Max Length: 30
    tag = models.CharField(
        name = 'tag',
        max_length = 15,
        help_text = 'Max Length: 15',
        blank = True,
        default = 'general',
    )

    # Tag color | Max Length: 15
    COLOR_CHOICES = (
        ['INDIGO', 'indigo'],
        ['GREEN', 'green'],
        ['RED', 'red'],
        ['PURPLE', 'purple'],
        ['PINK', 'pink'],
        ['LIME', 'lime'],
        ['TEAL', 'teal'],
        ['CYAN', 'cyan']
    )
    color = models.CharField(
        name = 'color',
        max_length = 15,
        choices = COLOR_CHOICES,
        default = COLOR_CHOICES[0][0],
    )

    # Content | Max Length: 500
    content = models.TextField(
        name = 'content',
        max_length = 500,
        help_text = 'Max Length: 500',
    )

    # Starred | Boolean
    starred = models.BooleanField(
        name = 'starred',
        default = 0,
        null = True,
        blank = True,
    )

    # Date_Modified | Datetime
    date_modified = models.DateTimeField(
        name = 'date_modified',
        verbose_name = 'Modified Date'
    )

    # User Id  | Foreign Key (CoreUser.id)
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)

    class Meta:
        managed = True          # Allow Create, Delete
        db_table = 'dashboard_reservedmessages'