from django import forms
from django.core.validators import RegexValidator


class UserForm(forms.Form):
    ''' Inherited from core.models.CoreUser '''
    
    firstname = forms.CharField(max_length = 30, label = "Firstname", required = True, help_text = 'Max Length: 30', error_messages = {'required': 'This field is required'}, validators = [RegexValidator('^[A-Za-z ]+$', message = "Letters allowed only!")])
    lastname = forms.CharField(max_length = 30, label = "Lastname", required = True, help_text = 'Max Length: 30', error_messages = {'required': 'This field is required'}, validators = [RegexValidator('^[A-Za-z ]+$', message = "Letters allowed only!")])
    username = forms.CharField(label = "Username", disabled = True, required = False)
    email_address = forms.CharField(label = "Email Address", disabled = True, required = False)
    phone_number = forms.CharField(max_length = 12, label = "Phone Number", required = True, help_text = 'format: XXXX XXX XXX', error_messages = {'required': 'This field is required'}, validators = [RegexValidator('^[0-9 ]+$', message = "Numbers allowed only!")])
    role = forms.CharField(max_length = 5, label = "Role", disabled = True, required = False)
    site_name = forms.CharField(label = "Associated Site", disabled = True, required = False)
    country = forms.CharField(max_length = 30, label = "Country", help_text = 'Max Length: 30', validators = [RegexValidator('^[A-Za-z ]+$', message = "Letters allowed only!")])
    city = forms.CharField(max_length = 30, label = "City", help_text = 'Max Length: 30', validators = [RegexValidator('^[A-Za-z ]+$', message = "Letters allowed only!")])
    bio = forms.CharField(max_length = 75, label = "Bio", help_text = 'Max Length: 75')
    profile_image = forms.FileField(label = 'Profile picture', required = False, help_text = 'Size < 1M', validators = [1024 * 1024])