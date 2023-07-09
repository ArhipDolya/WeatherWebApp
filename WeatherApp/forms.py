from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterUserForm(UserCreationForm):

    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=30) 

    class Meta():
        model = User
        fields = ['username', 'email', 'password1', 'password2']