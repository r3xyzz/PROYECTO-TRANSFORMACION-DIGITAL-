from django.contrib import admin
from .models import Sala, Reserva

# Registrar modelos
admin.site.register(Sala)
admin.site.register(Reserva)