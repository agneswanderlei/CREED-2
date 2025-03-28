from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        raise forms.ValidationError(
            "Senha e usuário incorreto! Por favor entre em contato com o Administrador",
            code="invalid_login",
        )
