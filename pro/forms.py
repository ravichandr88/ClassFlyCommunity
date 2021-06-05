from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
import re
from user.models import OTP


#Function to validate Phone Number
def validate_not_mobile(value):

    rule = re.compile(r'(^[+0-9]{1,3})*([0-9]{10,11}$)')

    if not rule.search(value):
       return False
    elif len(value) != 10:
        return False

    return True

#Class to add Bootstrap for input fields in HTML
class BootstrapModelForm(forms.Form):
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
            
            

class SignupForm( UserCreationForm , BootstrapModelForm):
    
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
    
    class Media:
        js = ('login/js/signup.js',)
# name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class' : 'input100'}),required=True,help_text='Your name')
    

class SMSotpForm(BootstrapModelForm):
    
    otp = forms.CharField(max_length=4)

    
    class Meta:
        fields = ['otp',]
        icons = {'otp': 'fa fa-unlock-alt',}
        place_holder = {'otp':'Enter 4 digit code'}

    class Media:
        js = ('login/js/otp.js',)


class LoginForm(BootstrapModelForm):
    phone_number = forms.CharField(required = True)
    password = forms.CharField(required = True, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(LoginForm,self).clean()
        phone_number = self.cleaned_data.get('phone_number')
        #Check whether username exists or not
        user = None
        try:
            user = User.objects.get(username=phone_number)
        except:
              self.add_error('phone_number', 'Phone Number not found')

        #Check whether user account is active or not
        if not user.is_active:
             self.add_error('phone_number', 'OTP not confirmed')
             self.redirect = True

        return cleaned_data

    class Meta:
        field = ['phone_number','password']
        icons = {'phone_number':'fa fa-mobile','password':'fa fa-lock'}
        place_holder = {'phone_number':'Enter phone number','password':'Enter Password'}

    class Media:
        js = ('login/js/login.js',)



class ResetPasswordForm(BootstrapModelForm):
    phone_number = forms.CharField(required = True)

    def clean(self):
        cleaned_data = super(BootstrapModelForm,self).clean()
        phone_number = self.cleaned_data.get('phone_number')
        #Check whether username exists or not
        user = None
        try:
            user = User.objects.get(username=phone_number)
        except:
              self.add_error('phone_number', 'Phone Number not found')

        return cleaned_data

    class Meta:
        field = ['phone_number']
        icons = {'phone_number':'fa fa-mobile'}
        place_holder = {'phone_number':'Enter phone number'}


class PasswordResetForm(BootstrapModelForm):
    password = forms.CharField(required = True, widget=forms.PasswordInput(),label='Password')
    confirm_password = forms.CharField(required = True, widget=forms.PasswordInput(),label='Confirm Password')

    def clean(self):
        cleaned_data = super(BootstrapModelForm,self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        #Check whether both passwords are same
        if password != confirm_password:
            self.add_error('password', 'Passowrda are not same')      

        return cleaned_data

    class Meta:
        field = ['password','confirm_password']
        icons = {'phone_number':'fa fa-mobile'}
        place_holder = {'phone_number':'Enter phone number'}