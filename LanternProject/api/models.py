from django.db import models

from core.models import CoreSite

class ApiCustomization(models.Model):
    ''' Api Site Customization '''

    # Title | Max Length: 20
    title = models.CharField(
        name = 'title',
        max_length = 20,
        default = 'Hello There!',
    )

    # Placeholder | Max Length: 40
    placeholder = models.CharField(
        name = 'placeholder',
        max_length = 40,
        default = 'Ask us anything, or share your feedback.',
    )

    # LiveChat Title | Max Length: 20
    livechat_title = models.CharField(
        name = 'livechat_title',
        max_length = 20,
        default = 'Start a Conversation',
    )

    # LiveChat Placeholder | Max Length: 30
    livechat_placeholder = models.CharField(
        name = 'livechat_placeholder',
        max_length = 30,
        default = 'We are ready to assist',
    )

    # Ticket Title | Max Length: 20
    livechat_ticket = models.CharField(
        name = 'ticket_title',
        max_length = 20,
        default = 'Leave a Ticket',
    )

    # Ticket Placeholder | Max Length: 30
    ticket_placeholder = models.CharField(
        name = 'ticket_placeholder',
        max_length = 30,
        default = 'We will contact you by email.',
    )

    # Virtual Agent Title | Max Length: 20
    virtualagent_ticket = models.CharField(
        name = 'virtualagent_title',
        max_length = 20,
        default = 'Virtual Agent',
    )

    # Virtual Agent Placeholder | Max Length: 30
    virtualagent_placeholder = models.CharField(
        name = 'virtualagent_placeholder',
        max_length = 30,
        default = 'Try our AI powered agent.',
    )

    # Site Id | Foreign Key (CoreSite.id)
    site = models.ForeignKey(CoreSite, models.DO_NOTHING)

    class Meta:
        managed = True          # Allow Create, Delete
        db_table = 'api_customization'


class ApiTitle(models.Model):
    ''' Api Title '''

    # Title | Max Length: 30
    title = models.CharField(
        name = 'title',
        max_length = 30,
    )

    # Customization Id | Foreign Key (CoreSite.id)
    customization = models.ForeignKey(ApiCustomization, models.DO_NOTHING)

    class Meta:
        managed = True          # Allow Create, Delete
        db_table = 'api_title'