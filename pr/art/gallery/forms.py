from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordResetForm,
    SetPasswordForm
)
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите логин (имя пользователя или E-mail)',
            'class': 'form-input'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль',
            'class': 'form-input'
        })
    )

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Введите E-mail',
            'class': 'form-input'
        })
    )
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите логин (имя пользователя)',
            'class': 'form-input'
        })
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль',
            'class': 'form-input'
        })
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Подтвердите пароль',
            'class': 'form-input'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

class WorkRegistrationForm(forms.Form):
    name = forms.CharField(
        label='Имя автора / псевдоним',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите имя автора',
            'class': 'form-input'
        })
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Введите E-mail',
            'class': 'form-input'
        })
    )
    phone = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите номер телефона',
            'class': 'form-input'
        })
    )
    portfolio = forms.URLField(
        label='Портфолио',
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'Вставьте ссылку на свое портфолио',
            'class': 'form-input'
        })
    )
    file = forms.FileField(
        label='Файл работы',
        widget=forms.FileInput(attrs={
            'class': 'form-input'
        })
    )

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Введите E-mail',
            'class': 'form-input'
        })
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль',
            'class': 'form-input'
        })
    )
    new_password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль повторно',
            'class': 'form-input'
        })
    )

from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']