from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, PasswordInput
from secrets import token_bytes

from .models import Nickname, Sektant, Sekta, Vacancy


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = Sektant
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'логин'
        self.fields['username'].label = 'Логин'
        self.fields['password'].widget.attrs['placeholder'] = 'пароль'
        self.fields['password'].label = 'Пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'login-form-{field_name}'

        self.error_messages = {
            'invalid_login': (
                "Введите корректные имя пользователя и пароль"
            ),
        }


class RegisterForm(ModelForm):
    username = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'placeholder': 'логин'}),
        label='Логин', error_messages={'unique': 'Пользователь с таким именем уже зарегистрирован'})
    password = forms.CharField(
        widget=PasswordInput(attrs={'placeholder': 'пароль'}), label='Пароль')
    can_be_invited = forms.BooleanField(
        required=False, label='Разрешить приглашать меня в секты')

    class Meta:
        model = Sektant
        fields = ["username", "password", "can_be_invited"]
        
    def save(self, *args, commit=True, **kwargs):
        sektant = super().save(*args, commit=commit, **kwargs)
        sektant.set_password(self.cleaned_data['password'])
        if commit:
            sektant.save()
        return sektant


class SektaCreationForm(ModelForm):
    sektaname = forms.CharField(max_length=100, label='Название секты')
    can_has_vacancy = forms.BooleanField(
        required=False, label='Разрешить вступать по пригласительному токену')

    class Meta:
        model = Sekta
        fields = ['sektaname', 'description']

    def save(self, user):
        sekta = Sekta(creator=user, sektaname=self.cleaned_data['sektaname'],
                      description=self.cleaned_data['description'], private_key=token_bytes(16))
        sekta.save()
        return sekta


class TokenInputForm(ModelForm):
    nickname = forms.CharField(label='Тайное имя')

    class Meta:
        model = Vacancy
        fields = ['sekta', 'token']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['sekta'].label = 'Секта'
        self.fields['token'].label = 'Пригласительный токен'

    def save(self, user):
        sekta = self.cleaned_data['sekta']
        nickname = Nickname(sekta=sekta, sektant=user, nickname=self.cleaned_data['nickname'])
        nickname.save()
