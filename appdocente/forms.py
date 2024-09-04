from django import forms
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    email = forms.EmailField(label="Correo Institucional", max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        valid_domains = ["@duocuc.cl", "@profesor.duoc.cl", "@profesorduoc.cl"]
        if not any(email.endswith(domain) for domain in valid_domains):
            raise ValidationError("El correo debe ser institucional.")
        return email
