from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
# from .models import Sala,Reserva                              SE COMENTA POR NUEVA BD
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # Primero intenta autenticar usando el nombre de usuario
        user = authenticate(username=username, password=password)
        
        # Si no encuentra usuario, intenta autenticar usando el correo electrónico
        if user is None:
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is None:
            raise forms.ValidationError("Usuario o contraseña incorrectos.")
        self.cleaned_data['user'] = user
        return self.cleaned_data

class recintosForm(forms.Form):
    calendario_fecha_inicio = forms.DateField(
        label='Fecha de Inicio',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    calendario_fecha_final = forms.DateField(
        label='Fecha Final',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    archivo_csv = forms.FileField(label='Seleccione un archivo CSV')