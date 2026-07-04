from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    avatar = forms.ImageField(required=True, label='Аватар')

    class Meta:
        model = User
        fields = ('username', 'avatar', 'password1', 'password2')