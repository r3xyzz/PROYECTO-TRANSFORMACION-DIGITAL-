from django.contrib import admin
from .models import Sala, Reserva, UserProfile

# Registrar modelos
admin.site.register(Sala)
admin.site.register(Reserva)
admin.site.register(UserProfile)