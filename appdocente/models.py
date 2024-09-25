from django.db import models
from django.contrib.auth.models import User

# Modelo para las salas
class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_sala = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Modelo para las reservas
class Reserva(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    nombre_evento = models.CharField(max_length=200)
    denominacion_evento = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.nombre_evento} - {self.sala} ({self.fecha_inicio})"

    class Meta:
        ordering = ['-fecha_inicio', 'hora_inicio']  # Ordenar por fecha de inicio descendente y hora de inicio

# Perfil de usuario
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Coordinador General Docente', 'Coordinador General Docente'),
        ('Coordinadora Docente', 'Coordinadora Docente'),
        ('Asistente de Coordinación Docente', 'Asistente de Coordinación Docente'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    
    def __str__(self):
        return f'{self.user.username} - {self.role}'

