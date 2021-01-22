from django.contrib.auth.forms import UserCreationForm
from django import forms
from registration.forms import RegistrationForm

from .models import User


class RegForm(RegistrationForm):
    first_name = forms.CharField(
        required=True, max_length=150, label="Имя",
        widget=forms.TextInput(attrs={'placeholder': 'Иван'}))
    last_name = forms.CharField(required=True, max_length=150, label="Фамилия")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',
                  'password1', 'password2')
        help_texts = {
            'username': ('<ul><li>Не более 150 символов.</li>'
                         '<li>Только буквы, цифры и символы '
                         '@/./+/-/_.</li></ul>'),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Иван'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Иванов'})
        self.fields['username'].widget.attrs.update({'placeholder': 'login'})
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'ivan@yandex.ru'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'пароль'})
        self.fields['password2'].widget.attrs.update(
            {'placeholder': 'повторите пароль'})
