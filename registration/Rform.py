from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django import forms
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    
    email = forms.EmailField()

    first_name = forms.CharField(max_length=30)

    last_name = forms.CharField(max_length=30)

    hourly = forms.FloatField(label="Hourly (CDN)")

    reg_key = forms.CharField(max_length=20, label="Registration Key")

    class Meta:

        model = User
        fields = ["username", "email","first_name", "last_name", "password1", "password2"]