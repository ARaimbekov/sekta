from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, PasswordInput

from .models import Sektant

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = Sektant
        fields = ('username', 'password')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'логин'
        self.fields['password'].widget.attrs['placeholder'] = 'пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'login-form-{field_name}'

        self.error_messages = {
            'invalid_login': (
                "Введите корректные имя пользователя и пароль"
            ),
        }

class RegisterForm(ModelForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=PasswordInput())

    class Meta:
        model = Sektant
        fields = ["username", "password"]

    def save(self, *args, commit=True, **kwargs):
        sektant = super().save(*args, commit=commit, **kwargs)
        sektant.set_password(self.cleaned_data['password'])
        if commit:
            sektant.save()
        return sektant
