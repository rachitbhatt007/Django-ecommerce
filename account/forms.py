from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class UserRegisterForm2(ModelForm):
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea())
    
    class Meta:
        model = UserProfile
        fields = ['mobilephone']


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
