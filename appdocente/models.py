from django.db import models

class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_sala = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    nombre_evento = models.CharField(max_length=200)
    denominacion_evento = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.nombre_evento} - {self.sala} ({self.fecha_inicio})"