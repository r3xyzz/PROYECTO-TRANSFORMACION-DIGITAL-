from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
# from .models import Sala,Reserva                              SE COMENTA POR NUEVA BD
from .models import CSVFile

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class CSVForm(forms.ModelForm):
    class Meta:
        model = CSVFile
        fields = ['nombre', 'archivo']

    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if not archivo.name.endswith('.csv'):
            raise forms.ValidationError('Solo se permiten archivos CSV.')
        return archivo

class SalaForm(forms.ModelForm):
    ''
    # class Meta:
    #     model = Sala                                          SE COMENTA POR NUEVA BD
    #     fields = ['nombre', 'tipo', 'capacidad']
