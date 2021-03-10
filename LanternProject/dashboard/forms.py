from django import forms
from .models import ReservedMessages, User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class ProfileForm(forms.ModelForm):
    ''' Profile form '''    

    class Meta:
        model = User

        # Used fields
        # fields = ['firstname', 'lastname', 'email', 'username', 'phonenumber', 'role']
        fields = ['first_name', 'last_name', 'email', 'username', 'phonenumber']        

        # Error messages
        error_messages = {
            'max_length': 'Field is too long!',
            'required': 'This field is required',
        }


    # Override HTML attributes
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # for field in ['username', 'email', 'role']:
        for field in ['username', 'email']:
            self.fields[field].disabled = True
            self.fields[field].required = False


class LoginForm(forms.Form):
    ''' Login Form '''

    email = forms.EmailField(
        max_length = 50,
        label = 'email',
        help_text = 'Max length: 50',
        )

    password = forms.CharField(
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
        self.fields['email'].type = 'email'
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


class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email')

class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email')