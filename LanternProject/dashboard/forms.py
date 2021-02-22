from django import forms
from core.models import CoreUser


class ProfileForm(forms.ModelForm):
    ''' Profile form '''    

    class Meta:
        model = CoreUser

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


class LoginForm(forms.ModelForm):
    ''' Login Form '''

    # Custome fields
    remember_me = forms.BooleanField(
        label = 'Remember me' 
    )

    class Meta:
        model = CoreUser        

        # Used fields
        fields = ['email', 'password']        

        # Error messages
        error_messages = {
            'max_length': 'Field is too long!',
            'required': 'This field is required',
        }


    # Override HTML attributes
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ['email', 'password']:
            self.fields[field].type = field

        self.fields['remember_me'].type = 'checkbox'