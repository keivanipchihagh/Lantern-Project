from django import forms
from django.forms import widgets
from core.models import CoreUser


class Profile(forms.ModelForm):
    ''' Profile form '''    

    class Meta:
        model = CoreUser

        # Used fields
        fields = ['firstname', 'lastname', 'email', 'username', 'phonenumber', 'role', 'country', 'city', 'bio', 'image', 'site']

        # Error messages
        error_messages = {
            'max_length': 'Field is too long!',
            'required': 'This field is required',
        }


    # Override HTML attributes
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ['username', 'email', 'role', 'site']:
            self.fields[field].disabled = True
            self.fields[field].required = False