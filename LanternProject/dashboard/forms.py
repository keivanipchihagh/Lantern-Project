from django import forms
from core.models import CoreUser as User
from .models import DashboardReservedMessages as ReservedMessages


class ProfileForm(forms.ModelForm):
    ''' Profile form '''    

    class Meta:
        model = User

        # Used fields
        fields = ['firstname', 'lastname', 'email', 'username', 'phonenumber', 'role', 'country', 'city', 'bio']

        # Error messages
        error_messages = {
            'max_length': 'Field is too long!',
            'required': 'This field is required',
        }


    # Override HTML attributes
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ['username', 'email', 'role']:
            self.fields[field].disabled = True
            self.fields[field].required = False


class LoginForm(forms.Form):
    ''' Login Form '''

    email = forms.EmailField(
        max_length = 50,
        label = 'email',
        help_text = 'Max length: 50',
        error_messages = {
            'max_length': 'Maximum length is 50 characters',
            }
        )

    password = forms.CharField(
        max_length = 30,
        min_length = 8,
        label = 'password',
        help_text = 'Min length: 8',
        error_messages = {
            'min_length': 'Minimum length is 8 characters',
            'max_length': 'Maximum length is 30 characters',
            }
        )

    remember_me = forms.BooleanField(
        label = 'Remember me',
        required = False,
    )

    # Override HTML attributes
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ['email', 'password']:
            self.fields[field].type = field

        self.fields['remember_me'].type = 'checkbox'