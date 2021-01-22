from django.contrib.auth.forms import UserCreationForm
from django import forms
from registration.forms import RegistrationForm

from .models import User


class RegForm(RegistrationForm):
    first_name = forms.CharField(required=True, max_length=150, label="Имя")
    last_name = forms.CharField(required=True, max_length=150, label="Фамилия")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',
                  'password1', 'password2')
