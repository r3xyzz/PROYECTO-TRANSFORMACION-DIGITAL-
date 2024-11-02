import csv
from django.core.management.base import BaseCommand
from appdocente.models import ReporteFrecuencias
from datetime import datetime

class Command(BaseCommand):
    help = 'Carga datos desde un archivo CSV al modelo ReporteFrecuencias'

    def handle(self, *args, **kwargs):
        with open('frecuencias2.csv', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')  # Especifica el delimitador como punto y coma
            for row in reader:
                # Parseo de fechas y horas si es necesario
                fecha_inicio = datetime.strptime(row['FechaInicio'], '%d.%m.%Y').date()
                fecha_final = datetime.strptime(row['FechaFinal'], '%d.%m.%Y').date()
                hora_inicio = datetime.strptime(row['HoraInicio'], '%H:%M:%S').time()
                hora_fin = datetime.strptime(row['HoraFin'], '%H:%M:%S').time()
                
                # Creación del registro
                ReporteFrecuencias.objects.create(
                    evento=row['Evento'],
                    tipo_recurso=row['TipoRecurso'],
                    recurso=row['Recurso'],
                    recurso_extra=row['RecursoExtra'],
                    fecha_inicio=fecha_inicio,
                    fecha_final=fecha_final,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin,
                    cantidad_horas=row['CtdHoras'],
                    denominacion_evento=row['DenominacionEvento'],
                    fecha_final_extra=datetime.strptime(row['FechaFinalExtra'], '%d.%m.%Y').date(),
                    fecha_inicio_extra=datetime.strptime(row['FechaInicioExtra'], '%d.%m.%Y').date(),
                    evento_extra=row['EventoExtra'],
                    recurso_id=row['RecursoID'],
                    tipo_recurso_extra=row['TipoRecursoExtra'],
                    recurso_id_extra=row['RecursoIDExtra'],
                    tipo_recurso_id=row['TipoRecursoID']
                )
        self.stdout.write(self.style.SUCCESS('Datos cargados exitosamente'))