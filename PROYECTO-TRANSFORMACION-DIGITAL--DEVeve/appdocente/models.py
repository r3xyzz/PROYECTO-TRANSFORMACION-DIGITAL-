from django.db import models

# Create your models here.

class Cargo(models.Model):
    nombre_cargo = models.CharField(max_length=40)

    def __srt__(self):
        return self.nombre_cargo

class Usuario(models.Model):
    pnombre = models.CharField(max_length=40)
    snombre = models.CharField(max_length=40)
    appaterno = models.CharField(max_length=40)
    apmaterno = models.CharField(max_length=40)
    correo = models.CharField(max_length=60)
    password = models.CharField(max_length=20)
    id_cargo = models.ForeignKey(Cargo,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pnombre} {self.snombre} {self.appaterno} {self.apmaterno}'
    
class Sede(models.Model):
    nombre_sede = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_sede


class Categoria(models.Model):
    categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.categoria
    
class TipoRecinto(models.Model):
    tipo_recinto = models.CharField(max_length=100)

    def __str__(self):
        return self.tipo_recinto

class Recinto(models.Model):
    nombre_recinto = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    id_sede = models.ForeignKey(Sede,on_delete=models.CASCADE)
    id_categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    id_tipo = models.ForeignKey(TipoRecinto,on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_recinto
    
class Asignatura(models.Model):
    nombre = models.CharField(max_length=150)
    seccion = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.nombre} - {self.seccion}'
    
class Reserva(models.Model):
    id_usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    id_recinto = models.ForeignKey(Recinto,on_delete=models.CASCADE)
    id_asignatura = models.ForeignKey(Asignatura,on_delete=models.CASCADE)
    fecha = models.DateField()
    hra_inicio = models.CharField(max_length=10)
    hra_fin = models.CharField(max_length=10)
    estado = models.CharField(max_length=30) 
    
    def __str__(self):
        return f'Reserva de {self.id_usuario} en {self.id_recinto} para {self.id_asignatura}'



 
class CSVFile(models.Model):
    nombre = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='csvs/')
    subido_el = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


