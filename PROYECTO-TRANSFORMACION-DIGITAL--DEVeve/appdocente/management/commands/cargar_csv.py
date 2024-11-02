import csv
from django.core.management.base import BaseCommand
from appdocente.models import ReporteFrecuencias
from datetime import datetime

class Command(BaseCommand):
    help = 'Carga datos desde un archivo CSV al modelo ReporteFrecuencias'

    def handle(self, *args, **kwargs):
        with open('C:\\Users\\felip\\Downloads\\frecuencias2.csv', encoding='latin-1') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            
            # Lee el encabezado manualmente y verifica que esté correcto
            headers = next(reader)
            print("Encabezado detectado:", headers)
            
            for row in reader:
                # Asegúrate de que el número de columnas coincida con el encabezado
                if len(row) == len(headers):
                    data = dict(zip(headers, row))
                    
                    # Ahora puedes acceder a cada campo por su nombre
                    
                    cantidad_horas = data['CtdHoras'].replace(',', '.')
                    
                    print(f"Procesando registro: {data}")
                    print(f"Valor de FechaInicio: '{data['FechaInicio']}'")
                    
                    try:
                        if data['FechaInicio'].strip():  # Verifica si FechaInicio tiene valor
                            fecha_inicio = datetime.strptime(data['FechaInicio'].strip(), '%d.%m.%Y').date()
                        else:
                            print("FechaInicio está vacío, omitiendo este registro.")
                            continue  # Salta al siguiente registro si FechaInicio está vacío
                        
                        # Convertir otros campos de fecha y hora con el mismo patrón
                        fecha_final = (
                            datetime.strptime(data['FechaFinal'].strip(), '%d.%m.%Y').date()
                            if data['FechaFinal'].strip() else None
                        )
                        hora_inicio = (
                            datetime.strptime(data['HoraInicio'].strip(), '%H:%M:%S').time()
                            if data['HoraInicio'].strip() else None
                        )
                        hora_fin = (
                            datetime.strptime(data['HoraFin'].strip(), '%H:%M:%S').time()
                            if data['HoraFin'].strip() else None
                        )
                        fecha_final_extra = (
                            datetime.strptime(data['FechaFinalExtra'].strip(), '%d.%m.%Y').date()
                            if data['FechaFinalExtra'].strip() else None
                        )
                        fecha_inicio_extra = (
                            datetime.strptime(data['FechaInicioExtra'].strip(), '%d.%m.%Y').date()
                            if data['FechaInicioExtra'].strip() else None
                        )
                        
                        # Creación del registro en la base de datos
                        ReporteFrecuencias.objects.create(
                            evento=data['Evento'],
                            tipo_recurso=data['TpoRecurso'],
                            recursos=data['Recursos'],
                            recursos2=data['Recursos2'],
                            fecha_inicio=fecha_inicio,
                            fecha_final=fecha_final,
                            hora_inicio=hora_inicio,
                            hora_fin=hora_fin,
                            cantidad_horas=cantidad_horas,
                            denominacion_evento=data['DenominacionEvento'],
                            fecha_final_extra=fecha_final_extra,
                            fecha_inicio_extra=fecha_inicio_extra,
                            evento_extra=data['EventoExtra'],
                            recurso_id=data['RecursoID'],
                            tipo_recurso_2=data['TipoRecurso2'],
                            evento2=data['Evento2'],
                            recursos3=data['Recursos3'],
                            tipo_recurso_3=data['TipoRecurso3'],
                            tipo_recurso_4=data['TipoRecurso4']
                        )
                    except KeyError as e:
                        print(f"Error: La columna {e} no se encuentra en el archivo CSV")
                    except ValueError as e:
                        print(f"Error al convertir un valor: {e}")
        self.stdout.write(self.style.SUCCESS('Datos cargados exitosamente'))
        
        
#with open('C:\\Users\\felip\\Downloads\\frecuencias2.csv', encoding='latin-1') as csvfile: