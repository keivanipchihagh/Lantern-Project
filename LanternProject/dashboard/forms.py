from django import forms

class UserForm(forms.Form):
    ''' Inherited from core.models.CoreUser '''

    firstname = forms.CharField(max_length = 30, label = "Firstname", required = True, help_text = 'Max Length: 30', error_messages = {'required': 'This field is required'})
    lastname = forms.CharField(max_length = 30, label = "Lastname", required = True, help_text = 'Max Length: 30', error_messages = {'required': 'This field is required'})
    username = forms.CharField(max_length = 30, label = "Username", disabled = True)
    email_address = forms.CharField(max_length = 50, label = "Email Address", disabled = True)
    phone_number = forms.CharField(max_length = 12, label = "Phone Number", required = True, help_text = 'format: XXXX XXX XXX', error_messages = {'required': 'This field is required'})
    role = forms.CharField(max_length = 5, label = "Role", disabled = True)
    site_name = forms.CharField(max_length = 50, label = "Associated Site", disabled = True)
    country = forms.CharField(max_length = 30, label = "Country", help_text = 'Max Length: 30')
    city = forms.CharField(max_length = 30, label = "City", help_text = 'Max Length: 30')
    bio = forms.CharField(max_length = 75, label = "Bio", help_text = 'Max Length: 75')