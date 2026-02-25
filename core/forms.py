from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre de usuario'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña'})
    )

user = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField(
        label="Nombre Completo",
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Ej: MR. DogerBlue'})
    )
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'placeholder': 'Ingrese su correo electrónico'})
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña'})
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Repita su contraseña'})
    )



    def clean_username(self):
        username = self.cleaned_data['username']
        if user.objects.filter(username=username).exists():
            raise ValidationError("El nombre de usuario ya está en uso. Por favor, elige otro.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if user.objects.filter(email=email).exists():
            raise ValidationError("El correo electrónico ya está registrado. Por favor, elige otro.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden. Por favor, inténtalo de nuevo.")
        return cleaned_data

