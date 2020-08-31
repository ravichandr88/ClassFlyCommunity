from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput(attrs={'class': 'input'}))

    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'autofocus': True}),
            'email': forms.EmailInput(attrs={'class': 'input', 'required': True})
        }
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username
 
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    # Validating password
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
 
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")


class VideoUploadForm(forms.Form):
    title = forms.CharField(max_length=200)
    video_link = forms.CharField(max_length=1000)
    thumbnail_link = forms.CharField(max_length=1000)
    descripion = forms.TextInput()
    dept_head = forms.CharField(max_length=100)

    class Meta:
        fields = ['title', 'video_link','thumbnail_link','dept_head','descripion']
 

class Loginform(forms.Form):
    username = forms.CharField(max_length=100,required = True)
    password = forms.CharField(max_length=100,required = True)

    class Meta:
        fields = ['username','password']
 



