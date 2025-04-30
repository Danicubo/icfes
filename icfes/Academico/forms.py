from django import forms
from django.contrib.auth.forms import AuthenticationForm

class RegistroForm(forms.Form):
    documento = forms.CharField(label='Documento')
    nombre = forms.CharField(label='Nombres y apellidos')
    correo = forms.EmailField(label='Correo electrónico')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput)