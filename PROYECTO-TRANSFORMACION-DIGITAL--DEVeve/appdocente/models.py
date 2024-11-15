from django.db import models

# Create your models here.

class Cargo(models.Model):
    nombre_cargo = models.CharField(max_length=40)

    def __srt__(self):
        return self.nombre_cargo

class Reserva2(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    sala = models.CharField(max_length=100, db_column="SALA")
    fecha_inicio = models.DateField(db_column="FECHA_INICIO")
    fecha_final = models.DateField(db_column="FECHA_FINAL")
    hora_inicio = models.TimeField(db_column="HORA_INICIO")
    hora_final = models.TimeField(db_column="HORA_FINAL")
    correo = models.CharField(max_length=100, db_column="CORREO")
    estado = models.IntegerField(db_column="ESTADO")
    comentario = models.CharField(max_length=100, db_column="COMENTARIO")

    def __str__(self):
        return f"{self.estado} - {self.recurso} - {self.tipo_recurso} - {self.fecha_inicio} - {self.fecha_inicio} - {self.hora_inicio} - {self.hora_fin}"
    

class ReporteFrecuencias(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    evento = models.CharField(max_length=50, db_column='Evento')
    tipo_recurso = models.CharField(max_length=100, db_column='TipoRecurso')
    recursos = models.CharField(max_length=50, db_column='Recursos')
    recursos2 = models.CharField(max_length=100, db_column='Recursos2')
    fecha_inicio = models.DateField(db_column='FechaInicio')
    fecha_final = models.DateField(db_column='FechaFinal')
    hora_inicio = models.TimeField(db_column='HoraInicio')
    hora_fin = models.TimeField(db_column='HoraFin')
    cantidad_horas = models.DecimalField(max_digits=5, decimal_places=2, db_column='CtdHoras')
    denominacion_evento = models.CharField(max_length=100, db_column='DenominacionEvento')
    fecha_final_extra = models.DateField(db_column='FechaFinalExtra')
    fecha_inicio_extra = models.DateField(db_column='FechaInicioExtra')
    evento_extra = models.CharField(max_length=50, db_column='EventoExtra')
    recurso_id = models.CharField(max_length=50, db_column='RecursoID')
    tipo_recurso_2 = models.CharField(max_length=50, db_column='TipoRecurso2')
    evento2 = models.CharField(max_length=50, db_column='Evento2')
    recursos3 = models.CharField(max_length=50, db_column='Recursos3')
    tipo_recurso_3 = models.CharField(max_length=50, db_column='TipoRecurso3')
    tipo_recurso_4 = models.CharField(max_length=50, db_column='TipoRecurso4')
    
    class Meta:
        db_table = 'reporte_frecuencias'
    
    
class Recintos(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    tipo_recurso = models.CharField(max_length=100, db_column='tipo_recurso')
    sala = models.CharField(max_length=100, db_column='sala')
    nombre_recinto = models.CharField(max_length=100, db_column='nombre_recinto')
    capacidad = models.IntegerField(db_column='capacidad')
    fecha_inicio = models.DateField(db_column='fecha_inicio')
    fecha_final = models.DateField(db_column='fecha_final')
    hora_inicio = models.TimeField( db_column='hora_inicio')
    hora_final = models.TimeField(db_column='hora_final')
    cantidad_modulos = models.IntegerField(db_column='cantidad_modulos')
    denominacion_evento = models.CharField(max_length=100, db_column='denominacion_evento')
    id_evento = models.IntegerField(db_column='id_evento')
    id_recurso = models.IntegerField(db_column='id_recurso')
    
    class Meta:
        db_table = 'recintos'


