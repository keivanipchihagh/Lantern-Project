from django import forms
from core.models import CoreUser as User
from .models import DashboardReservedMessages as ReservedMessages


class ProfileForm(forms.ModelForm):
    ''' Profile form '''    

    class Meta:
        model = User

        # Used fields
        fields = ['firstname', 'lastname', 'emailaddress', 'username', 'phonenumber', 'role']

        # Error messages
        error_messages = {
            'max_length': 'Field is too long!',
            'required': 'This field is required',
        }


    # Override HTML attributes
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ['username', 'emailaddress', 'role']:
            self.fields[field].disabled = True
            self.fields[field].required = False


class LoginForm(forms.Form):
    ''' Login Form '''

    emailaddress = forms.EmailField(
        max_length = 50,
        label = 'emailaddress',
        help_text = 'Max length: 50',
        )

    password = forms.CharField(
        max_length = 30,
        min_length = 8,
        label = 'password',
        help_text = 'Min length: 8',
        )

    remember_me = forms.BooleanField(
        label = 'Remember me',
        required = False,
    )

    # Override HTML attributes
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['remember_me'].type = 'checkbox'
        self.fields['emailaddress'].type = 'email'
        self.fields['password'].type = 'password'


class ReservedMessagesForm(forms.ModelForm):

    class Meta:
        model = ReservedMessages

        fields = ['title', 'tag', 'color', 'starred', 'content']

        # Error messages
        error_messages = {
            'max_length': 'Field is too long!',
            'required': 'This field is required',
        }