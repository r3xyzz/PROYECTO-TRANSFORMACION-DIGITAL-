from django.db import models
from django.contrib.auth.models import User
import datetime
from django.urls import reverse
from django.utils import timezone

class Sala(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    capacidad = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    nombre_evento = models.CharField(max_length=100)
    denominacion_evento = models.CharField(max_length=200, blank=True, null=True)
    fecha_inicio = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.nombre_evento} in {self.sala}"

class CSVFile(models.Model):
    nombre = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='csvs/')
    subido_el = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Peticiones(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre