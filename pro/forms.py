from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
import re

#Function to validate Phone Number
def validate_not_mobile(value):

    rule = re.compile(r'(^[+0-9]{1,3})*([0-9]{10,11}$)')

    if not rule.search(value):
       return False
    elif len(value) != 10:
        return False

    return True

#Class to add Bootstrap for input fields in HTML
class BootstrapModelForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        icons = getattr(self.Meta, 'icons', dict())
        place_holder = getattr(self.Meta, 'place_holder', dict())

        for field_name, field in self.fields.items():
            # add form-control class to all fields
            field.widget.attrs['class'] = 'input100'
            # set icon attr on field object
            if field_name is 'username':
                field.label = 'Phone Number'
            if field_name in icons:
                field.icon = icons[field_name]
            if field_name in place_holder:
                field.widget.attrs['placeholder'] = place_holder[field_name]

class SignupForm(BootstrapModelForm):
    
    def clean(self):
        cleaned_data = super(UserCreationForm,self).clean()
        t = self.cleaned_data.get('username')
        if not validate_not_mobile(t):
            self.add_error('username', 'Not a valid phone number')
        return cleaned_data
    
    class Meta:
        model = User
        fields = ['username','first_name','password1','password2']
        icons = {'password1': 'fa fa-lock','username':'fa fa-mobile','password2':'fa fa-lock','first_name':'fa fa-user'}
        place_holder = {'password1':'Min 8 characters','username':'Phone Number','password2':'Re-Enter Password'}
# name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class' : 'input100'}),required=True,help_text='Your name')
    