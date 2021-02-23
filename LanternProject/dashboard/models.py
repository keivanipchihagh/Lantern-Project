from django.db import models


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