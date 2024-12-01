from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password = forms.CharField(max_length=50,
                               required=True,
                               label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    remember_me = forms.BooleanField(required=False, label='Запомнить меня', widget=forms.CheckboxInput())
