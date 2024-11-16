import json
import csv
from django.http import JsonResponse, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views import generic
from .models import Reserva2, Recintos
from .forms import LoginForm, recintosForm  # Import CSVForm
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from datetime import datetime, timedelta
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .decorators import group_required
from django.core.paginator import Paginator
import chardet
from django.db import connection
from django.db.models import Q
from django.http import HttpResponseRedirect
import configparser, os

def obtener_fechas_ini():
    
    
    ruta_archivo = os.path.join(os.path.dirname(__file__), 'config', 'calendario.ini')

    # Crear una instancia de ConfigParser
    config = configparser.ConfigParser()

    # Verificar si el archivo ya existe y si la sección 'configuracion' existe
    if not os.path.exists(ruta_archivo):
        # Si el archivo no existe, crearlo y agregar la sección
        config.add_section('configuracion')
        
    config.read(ruta_archivo)
    
    fecha_inicio = config.get('configuracion', 'fecha_inicio')
    fecha_final = config.get('configuracion', 'fecha_final')

    # Convertir las fechas de 'día/mes/año' a objetos datetime
    fecha_inicio_dt = datetime.strptime(fecha_inicio, '%d/%m/%Y')
    fecha_final_dt = datetime.strptime(fecha_final, '%d/%m/%Y')

    return fecha_inicio_dt, fecha_final_dt

def obtener_semanas_restantes():
    """
    Obtiene las semanas restantes del año, pero solo dentro del rango de fechas
    'fecha_inicio' y 'fecha_final' obtenidas desde el archivo INI. Descartando las semanas ya pasadas
    pero incluyendo la semana actual si hoy está dentro de ella.
    """
    # Obtener las fechas de inicio y final desde el archivo INI
    fecha_inicio, fecha_final = obtener_fechas_ini()

    hoy = datetime.today()
    fin_ano = datetime(hoy.year, 12, 31)  # 31 de diciembre del año actual

    semanas = []  # Lista para almacenar las semanas

    # Inicia desde el lunes de la semana de 'fecha_inicio' o la fecha de inicio
    if fecha_inicio.weekday() == 0:  # Lunes
        inicio_semana = fecha_inicio
    else:
        inicio_semana = fecha_inicio - timedelta(days=fecha_inicio.weekday())

    while inicio_semana <= fecha_final:
        # Calcular el fin de la semana
        fin_semana = inicio_semana + timedelta(days=6)

        # Incluir la semana si la fecha actual está dentro de ella (o si está en el futuro)
        if inicio_semana <= hoy <= fin_semana:
            inicio_formateado = inicio_semana.strftime('%d/%m/%Y')
            fin_formateado = fin_semana.strftime('%d/%m/%Y')
            semanas.append(f"{inicio_formateado} - {fin_formateado}")
        # Si la semana está en el futuro y no ha pasado, agregarla
        elif inicio_semana > hoy:
            inicio_formateado = inicio_semana.strftime('%d/%m/%Y')
            fin_formateado = fin_semana.strftime('%d/%m/%Y')
            semanas.append(f"{inicio_formateado} - {fin_formateado}")

        # Avanzar a la siguiente semana
        inicio_semana += timedelta(days=7)

    return semanas

# Ocupar landing al momento de hacer logout
def landing(request):
    template = loader.get_template('landing.html')
    return HttpResponse(template.render())

@login_required
def bienvenida(request):
    return render(request, 'bienvenida.html')

def subir_archivo(request):

    if request.method == "POST":
        
        form = recintosForm(request.POST, request.FILES)
        if form.is_valid():
            
            
            ruta_archivo = os.path.join(os.path.dirname(__file__), 'config', 'calendario.ini')

            # Crear una instancia de ConfigParser
            config = configparser.ConfigParser()

            # Verificar si el archivo ya existe y si la sección 'configuracion' existe
            if not os.path.exists(ruta_archivo):
                # Si el archivo no existe, crearlo y agregar la sección
                config.add_section('configuracion')

            # Leer el archivo .ini
            config.read(ruta_archivo)
            
            fecha_inicio = request.POST.get('calendario_fecha_inicio')
            fecha_final = request.POST.get('calendario_fecha_final')

            # Convertir las fechas a formato 'día/mes/año' (ejemplo: 06/12/2024)
            fecha_inicio_formateada = datetime.strptime(fecha_inicio, '%Y-%m-%d').strftime('%d/%m/%Y')
            fecha_final_formateada = datetime.strptime(fecha_final, '%Y-%m-%d').strftime('%d/%m/%Y')


            # Actualizar las fechas en la sección 'configuracion'
            config.set('configuracion', 'fecha_inicio', fecha_inicio_formateada)  # Aquí pasas las fechas desde el formulario
            config.set('configuracion', 'fecha_final', fecha_final_formateada)

            # Guardar los cambios en el archivo calendario.ini
            with open(ruta_archivo, 'w') as configfile:
                config.write(configfile)
            
            
            registros_insertados = 0
            
            """"
            with connection.cursor() as cursor:
                cursor.execute("TRUNCATE TABLE recintos")
        
            archivo_csv = request.FILES['archivo_csv']

            decoded_file = archivo_csv.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file, delimiter=';')
            
                
            next(reader) 
            for row in reader:
                
                fecha_inicio = datetime.strptime(row[4], '%d-%m-%Y').date()
                fecha_final = datetime.strptime(row[5], '%d-%m-%Y').date()
                
                # Ajustar el formato de hora
                hora_inicio = datetime.strptime(row[6], '%H:%M:%S').time()
                hora_final = datetime.strptime(row[7], '%H:%M:%S').time()
                        
                Recintos.objects.create(
                    tipo_recurso=row[0],
                    sala=row[1],
                    nombre_recinto=row[2],
                    capacidad=row[3],
                    fecha_inicio=fecha_inicio,
                    fecha_final=fecha_final,
                    hora_inicio=hora_inicio,
                    hora_final=hora_final,
                    cantidad_modulos=row[8],
                    denominacion_evento=row[9],
                    id_evento=row[10],
                    id_recurso=row[11]
                )
                
                registros_insertados += 1
                """
            
                
            messages.success(request, f'Datos cargados con éxito. Se han registrado {registros_insertados} filas.')
            return redirect('subir_archivo')  # Cambia si es necesario
        
    else:
        form = recintosForm()
    
    return render(request, 'subir_archivo.html', {'form': form})


def no_autorizado(request):
    return render(request, 'no_autorizado.html')

@login_required
@group_required('encargado')
def reservas(request):
    correo2 = request.GET.get('correo', '')  # Obtiene el correo desde la URL (parámetro GET)
    
    # Si es una solicitud POST, actualizar el estado de la reserva
    if request.method == 'POST':
        reserva_id = request.POST.get('reserva_id')
        accion = request.POST.get('accion')  # Puede ser 'aprobar' o 'rechazar'
        
        # Obtiene la reserva específica
        reserva = get_object_or_404(Reserva2, id=reserva_id)
        
        if accion == 'aprobar':
            
            # Ver si hay conflicto de horario
            conflicto = Reserva2.objects.filter(
                fecha_inicio=reserva.fecha_inicio,
                estado=1,  # El 1 es las que están aprobadas
                sala=reserva.sala  # Para revisar solo en la misma sala
            ).exclude(id=reserva.id).filter(
                hora_inicio__lt=reserva.hora_final,  # lt significa menor que
                hora_final__gt=reserva.hora_inicio   # gt significa mayor que
            ).exists()

            if conflicto:
                messages.error(request, "Conflicto de horario: Ya existe una reserva aprobada en este rango de tiempo.")
            else:
                reserva.estado = 1  # Con 1 queda reservado
                reserva.save()
                messages.success(request, "Reserva aprobada con éxito.")
        
        elif accion == 'rechazar':
            reserva.estado = 2  # Con 2 queda rechazado
            reserva.save()
            messages.success(request, "Reserva rechazada con éxito.")
        
        return redirect('reservas')
    
    reservasUsuario = []

    # Esto busca por una parte del correo, pero si no se ingresa nada, cargan todos
    reservas = Reserva2.objects.filter(correo__icontains=correo2).order_by('-id') if correo2 else Reserva2.objects.all().order_by('-id')

    # Paginación
    paginator = Paginator(reservas, 10)  # 10 reservas por página
    page_number = request.GET.get('page')  # Obtiene el número de página de la URL
    page_obj = paginator.get_page(page_number)  # Obtiene las reservas para la página actual
    
    for res in page_obj:
        nombre_recinto = Recintos.objects.filter(sala=res.sala).values_list('nombre_recinto', flat=True).first()
        usuario = User.objects.filter(email=res.correo).values_list('first_name', 'last_name').first()
        nombre_completo = f"{usuario[0]} {usuario[1]}" if usuario else "Usuario no encontrado"
        
        reservasUsuario.append({
            'id': res.id,
            'docente': nombre_completo,
            'email': res.correo,
            'sala': res.sala,
            'nombre_recinto': nombre_recinto,
            'fecha_inicio': res.fecha_inicio,
            'hora_inicio': res.hora_inicio,
            'hora_final': res.hora_final,
            'estado': res.estado,
            'comentario': res.comentario
        })
    
    context = {
        "reservas": reservasUsuario,
        "correo": correo2,
        "page_obj": page_obj,  # Pasa el objeto de la página actual al template
    }
    
    return render(request, 'reservas.html', context)


def obtener_datos(request):
    ''
    # salas = Recinto.objects.all()
    # reservas = Reserva.objects.all()
    # reservas_json = list(reservas.values('fecha_inicio', 'hora_inicio', 'hora_fin', 'nombre_evento'))
    # return JsonResponse({'salas': list(salas.values()), 'reservas': reservas_json}, encoder=DjangoJSONEncoder)

@login_required
def obtener_horario_por_sala(request, sala_id):
    ''
    # # Filtrar las reservas para la sala seleccionada
    # reservas = Reserva.objects.filter(sala_id=sala_id).values('fecha_inicio', 'hora_inicio', 'hora_fin', 'nombre_evento')
    # return JsonResponse({'reservas': list(reservas)})









# ------------------------------------------- ESTE CODIGO YA VENIA COMENTADO --------------------

# def crear_reserva(request):
#     salas = Sala.objects.all()
#     if request.method == 'POST':
#         sala_id = request.POST.get('sala-id')  # Obtener el ID de la sala desde el campo oculto

#         # Verifica que el ID de la sala es un número
#         if not sala_id.isdigit():
#             return JsonResponse({'status': 'error', 'message': 'ID de sala no válido'}, status=400)

#         nombre_evento = request.POST.get('nombre-evento')
#         descripcion = request.POST.get('descripcion')
#         fecha_inicio = request.POST.get('fecha-ini')
#         hora_inicio = request.POST.get('hora-inicio')
#         hora_fin = request.POST.get('hora-fin')

#         # Validar y crear la reserva
#         sala = Sala.objects.get(id=int(sala_id))
#         reserva = Reserva(
#             sala=sala,
#             nombre_evento=nombre_evento,
#             denominacion_evento=descripcion,
#             fecha_inicio=fecha_inicio,
#             hora_inicio=hora_inicio,
#             hora_fin=hora_fin
#         )
#         reserva.save()
#         return JsonResponse({'status': 'success', 'message': 'Reserva creada exitosamente'})

#     context = {
#         'salas': salas,
#     }
#     return render(request, 'base.html', context)

# LOGIN PRINCIPAL (SOLO INICIO DE SESIÓN)
"""def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        contraseña = request.POST.get("password")   
        usuarios = Usuario.objects.all()
        emailValido = False
        passValida = False
        cargo = ''

        for usuario in usuarios:
            if usuario.correo == email and usuario.password == contraseña:
                emailValido = True
                passValida = True
                cargo = usuario.id_cargo.nombre_cargo 

        if emailValido and passValida:
            request.session["email"] = email
            print("Correo almacenado en sesión:", request.session["email"])  # Agrega esta línea para verificar
            if cargo == 'docente':
                return render(request, 'HomePageDocente.html')
            elif cargo == 'administrador':
                return render(request, 'bienvenida.html')
        else:
            mensaje = "Correo o password incorrecto"
            context = {'mensaje': mensaje}
            return render(request, "registration/login.html", context)

    return render(request, 'registration/login.html')"""


def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            print("login correcto")
            user = form.cleaned_data['user']
            auth_login(request, user)
            return redirect('Bienvenida')  # Redirige después del login
        else:
            print("error clave")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

#     ''
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password'
#             username = email.split('@')[0]  # Extrae el username del email

#     #         # Autenticar usuario
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('/bienvenida/')  # Redirige a la vista main.html si las credenciales son correctas
#             else:
#                 messages.error(request, 'Usuario o contraseña incorrectos. Verifica tus datos e intenta nuevamente.')
#         else:
#              messages.error(request, "Credenciales no válidas. Revisa el formato del correo institucional.")
#     else:
   

# CERRAR SESIÓN
def logout_view(request):
    logout(request)
    return redirect("login")

#apartado admin

def docentes(request):
    if request.method == 'POST':
        docente_id = request.POST.get('docente_id')
        print(f"docente_id recibido: {docente_id}")  # Verifica si se recibe el ID

        if docente_id:
            try:
                docente = User.objects.get(id=docente_id)
                docente.delete()  # Elimina al docente
                return redirect('docentes')  # Redirige después de eliminar al docente
            except User.DoesNotExist:
                pass  # Si no se encuentra el docente no hace nada

    # Obtener la lista de docentes
    docentes = []
    for u in User.objects.all():
        if u.groups.filter(name='docente').exists():
            docentes.append({
                'id': u.id,
                'nombre': u.first_name + ' ' + u.last_name,
                'correo': u.email
            })

    context = {"usuarios": docentes}
    return render(request, 'docentes.html', context)


# apartado docente 

def homeDocentes(request):
    return render(request,'HomePageDocente.html')

@login_required
@group_required('docente')
def reservar(request):
    
    email = request.user.email
    
    if request.method == 'GET':

        cap = request.GET.get('capacidad')
        sem_sel = request.GET.get('semana_seleccionada')
        sala = request.GET.get('sala')
        fecha = request.GET.get('semana')
        hora_inicio = request.GET.get('hora_inicio')
        hora_final = request.GET.get('hora_final')
        comentario = request.GET.get('comentario')

        # Si los parámetros están presentes en la URL, se procede con la validación
        if sala and fecha and hora_inicio and hora_final:
            
            conflictos = Recintos.objects.filter(
                sala=sala,
                fecha_inicio=fecha,  # Suponiendo que "fecha_inicio" almacena la fecha completa
            ).filter(
                # Superposición de horarios
                Q(hora_inicio__lte=hora_final) & Q(hora_final__gt=hora_inicio)
            )

            if conflictos.exists():
                # Hay al menos un conflicto
                messages.error(request, "El horario seleccionado ya está ocupado.")
            else:
                # No hay conflictos, puedes proceder
                
                conflicto = Reserva2.objects.filter(
                    fecha_inicio=fecha,
                    estado=1,  # El 1 es las que están aprobadas
                    sala=sala  # Para revisar solo en la misma sala
                ).filter(
                    hora_inicio__lt=hora_final,  # lt significa menor que
                    hora_final__gt=hora_inicio   # gt significa mayor que
                ).exists()

                if conflicto:
                    messages.error(request, "Conflicto de horario: Ya existe una reserva aprobada en este rango de tiempo.")
                else:
                    
                    if Recintos.objects.filter(sala=sala).exists():
                    
                        messages.success(request, "Horario disponible. Reserva confirmada.")

                        # Crear el nuevo registro de reserva
                        Reserva2.objects.create(
                            sala=sala,
                            fecha_inicio=datetime.strptime(fecha, '%Y-%m-%d').date(),
                            fecha_final=datetime.strptime(fecha, '%Y-%m-%d').date(),
                            hora_inicio=datetime.strptime(hora_inicio, '%H:%M').time(),
                            hora_final=datetime.strptime(hora_final, '%H:%M').time(),
                            correo=email,
                            estado=0,
                            comentario=comentario
                        )
                    else:
                        messages.error(request, "Error: La sala no existe.")
                
            
                
            return HttpResponseRedirect(reverse('reservar') + f'?sala={sala}&capacidad={cap}&semana_seleccionada={sem_sel}')

    hoy = datetime.today()
    
    weeks = obtener_semanas_restantes()

    #bloques de horas
    bloques_horarios = [
        {"hora_inicio": "08:00", "hora_final": "08:40"},
        {"hora_inicio": "08:40", "hora_final": "09:20"},
        {"hora_inicio": "09:30", "hora_final": "10:10"},
        {"hora_inicio": "10:10", "hora_final": "10:50"},
        {"hora_inicio": "11:00", "hora_final": "11:40"},
        {"hora_inicio": "11:40", "hora_final": "12:20"},
        {"hora_inicio": "12:30", "hora_final": "13:10"},
        {"hora_inicio": "13:10", "hora_final": "13:50"},
        {"hora_inicio": "14:00", "hora_final": "14:40"},
        {"hora_inicio": "14:40", "hora_final": "15:20"},
        {"hora_inicio": "15:30", "hora_final": "16:10"},
        {"hora_inicio": "16:10", "hora_final": "16:50"},
        {"hora_inicio": "17:00", "hora_final": "17:40"},
        {"hora_inicio": "17:40", "hora_final": "18:20"},
        {"hora_inicio": "18:20", "hora_final": "19:00"},
        {"hora_inicio": "19:10", "hora_final": "19:50"},
        {"hora_inicio": "19:50", "hora_final": "20:30"},
        {"hora_inicio": "20:40", "hora_final": "21:20"},
        {"hora_inicio": "21:20", "hora_final": "22:00"},
        {"hora_inicio": "22:10", "hora_final": "22:50"},
        {"hora_inicio": "22:50", "hora_final": "23:30"}
    ]
    
    #capacidades
    capacidades = Recintos.objects.values_list('capacidad', flat=True).distinct().order_by('capacidad')

    
    sala_seleccionada = request.GET.get('sala')
    capacidad_seleccionada = request.GET.get('capacidad')
    semana_seleccionada = request.GET.get('semana_seleccionada')
    
    #semana_seleccionada = "11/11/2024 - 17/11/2024"
    
    #calcular semana
    #inicio_semana = hoy - timedelta(days=hoy.weekday())  # lunes
    #fin_semana = inicio_semana + timedelta(days=5)  # sabado
    
    
    try:
        if semana_seleccionada:
            # Intentamos convertir la fecha de semana_seleccionada al formato adecuado
            inicio_semana = datetime.strptime(semana_seleccionada.split(' - ')[0], '%d/%m/%Y')
            fin_semana = datetime.strptime(semana_seleccionada.split(' - ')[1], '%d/%m/%Y')
        else:

            raise ValueError("Fecha no proporcionada")
    except (ValueError, TypeError):
        # Si ocurre un error, asignamos la semana actual
        
        print("aqui formateando")
        inicio_semana = hoy - timedelta(days=hoy.weekday())  # Lunes de la semana actual
        fin_semana = inicio_semana + timedelta(days=6)  # Sábado de la semana actual
        
        inicio_formateado = inicio_semana.strftime('%d/%m/%Y')
        fin_formateado = fin_semana.strftime('%d/%m/%Y')
        
        semana_seleccionada = f"{inicio_formateado} - {fin_formateado}"
        
        print(semana_seleccionada)
    

    # Ajuste para que fin_semana no cuente el domingo
    # Si el último día es domingo (domingo = 6), restamos un día
    if fin_semana.weekday() == 6:  # Domingo
        fin_semana = fin_semana - timedelta(days=1)
    
    if capacidad_seleccionada and capacidad_seleccionada.isdigit():
        capacidad_seleccionada = int(capacidad_seleccionada)

    filtros = {}
    filtros2 = {}
    if capacidad_seleccionada is not None:
        try:
            capacidad_seleccionada = int(capacidad_seleccionada)  # Intentamos convertir a entero
            filtros['capacidad'] = capacidad_seleccionada
            filtros2['capacidad'] = capacidad_seleccionada
        except ValueError:
            # Si la conversión falla, puedes manejarlo con un mensaje de error o simplemente no aplicar el filtro
            pass

# Obtener salas con el filtro de capacidad solo si es válido
    salasTotales = Recintos.objects.filter(**filtros).values_list('sala', flat=True).distinct()

    # Crear una lista de fechas para la semana actual (Lunes a Sábado)
    dias_semana = [(inicio_semana + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6)]

    # Crear un diccionario para almacenar la ocupación de cada bloque horario en cada día
    ocupacion_por_bloque = {}
    for dia in dias_semana:
        ocupacion_por_bloque[dia] = {}
        for bloque in bloques_horarios:
            ocupacion_por_bloque[dia][bloque["hora_inicio"]] = {"estado": "Libre", "fecha": dia}    


    if sala_seleccionada:
        
        if Recintos.objects.filter(sala=sala).exists():
        
            filtros2['sala'] = sala_seleccionada
            filtros2['fecha_inicio__gte'] = inicio_semana
            filtros2['fecha_inicio__lte'] = fin_semana
            
            
            # Filtrar las clases de la sala seleccionada para la semana actual
            clases = Recintos.objects.filter(
                **filtros2
            )

            # Actualizar la ocupación de los bloques de acuerdo a las clases encontradas
            for clase in clases:
                dia_semana = clase.fecha_inicio.strftime('%Y-%m-%d')
                hora_inicio_clase = clase.hora_inicio
                hora_final_clase = clase.hora_final

                # Verificar si el día está en dias_semana
                if dia_semana in dias_semana:
                    # Marcar todos los bloques que están en el rango de hora_inicio y hora_fin de la clase
                    for bloque in bloques_horarios:
                        bloque_inicio = datetime.strptime(bloque["hora_inicio"], "%H:%M").time()
                        bloque_fin = datetime.strptime(bloque["hora_final"], "%H:%M").time()

                        # Verificar si el bloque está dentro del rango de la clase
                        if (bloque_inicio >= hora_inicio_clase and bloque_inicio < hora_final_clase) or \
                        (bloque_fin > hora_inicio_clase and bloque_fin <= hora_final_clase) or \
                        (bloque_inicio <= hora_inicio_clase and bloque_fin >= hora_final_clase):
                            ocupacion_por_bloque[dia_semana][bloque["hora_inicio"]]["estado"] = "Ocupado"
                            ocupacion_por_bloque[dia_semana][bloque["hora_inicio"]]["fecha"] = dia_semana
                            ocupacion_por_bloque[dia_semana][bloque["hora_inicio"]]["descripcion"] = clase.denominacion_evento
                            print(ocupacion_por_bloque[dia_semana][bloque["hora_inicio"]]["fecha"])
                            
                            #print(f"Descripción asignada a {dia_semana} {bloque['hora_inicio']}: {clase.denominacion_evento}")  # Depuración
                            
            reservas = Reserva2.objects.filter(sala=sala_seleccionada, fecha_inicio__gte=inicio_semana, fecha_inicio__lte=fin_semana, estado=1)

            # Actualizar la ocupación con las reservas
            for reserva in reservas:
                dia_semana = reserva.fecha_inicio.strftime('%Y-%m-%d')
                hora_inicio_reserva = reserva.hora_inicio
                hora_final_reserva = reserva.hora_final

                # Verificar si el día está en dias_semana
                if dia_semana in dias_semana:
                    # Marcar los bloques reservados
                    for bloque in bloques_horarios:
                        bloque_inicio = datetime.strptime(bloque["hora_inicio"], "%H:%M").time()
                        bloque_fin = datetime.strptime(bloque["hora_final"], "%H:%M").time()

                        # Verificar si el bloque está dentro del rango de la reserva
                        if (bloque_inicio >= hora_inicio_reserva and bloque_inicio < hora_final_reserva) or \
                        (bloque_fin > hora_inicio_reserva and bloque_fin <= hora_final_reserva) or \
                        (bloque_inicio <= hora_inicio_reserva and bloque_fin >= hora_final_reserva):
                            ocupacion_por_bloque[dia_semana][bloque["hora_inicio"]]["estado"] = "Reservado"
                            ocupacion_por_bloque[dia_semana][bloque["hora_inicio"]]["fecha"] = dia_semana
                            ocupacion_por_bloque[dia_semana][bloque["hora_inicio"]]["descripcion"] = reserva.comentario
        else:
            sala_seleccionada = ''
            #messages.error(request, "La sala no existe.")

    print(semana_seleccionada)

    context = {
        "salas": salasTotales,
        "sala_seleccionada": sala_seleccionada,
        "capacidad_seleccionada": capacidad_seleccionada,
        "weeks": weeks,
        "semana_seleccionada": semana_seleccionada,
        "bloques_horarios": bloques_horarios,
        "ocupacion_por_bloque": ocupacion_por_bloque,
        "dias_semana": dias_semana, 
        "capacidades": capacidades
    }


    return render(request, 'reservar.html', context)


@login_required
@group_required('docente')
def mis_reservas(request):
    email = request.user.email

    # Esto solo se ejecuta si se quiere reservar
    if request.method == 'POST':
        sala = request.POST.get('sala')
        fecha = request.POST.get('semana')
        hora_inicio = request.POST.get('hora_inicio')
        hora_final = request.POST.get('hora_final')

        print(fecha)
        print(hora_inicio)
        print(hora_final)

        # Crear el nuevo registro de reserva
        Reserva2.objects.create(
            sala=sala,
            fecha_inicio=datetime.strptime(fecha, '%Y-%m-%d').date(),
            fecha_final=datetime.strptime(fecha, '%Y-%m-%d').date(),
            hora_inicio=datetime.strptime(hora_inicio, '%H:%M').time(),
            hora_final=datetime.strptime(hora_final, '%H:%M').time(),
            correo=email,
            estado=0
        )

        # Redirigir para que el código de abajo no trabaje
        return redirect('mis_reservas')

    # Si no se registra nada, cargará esto
    reservasUsuario = []
    reservas = Reserva2.objects.filter(correo=email).order_by('-id')

    # Paginación
    paginator = Paginator(reservas, 10)  # 10 reservas por página
    page_number = request.GET.get('page')  # Obtiene el número de página de la URL
    page_obj = paginator.get_page(page_number)  # Obtiene las reservas para la página actual

    for res in page_obj:
        nombre_recinto = Recintos.objects.filter(sala=res.sala).values_list('nombre_recinto', flat=True).first()

        reservasUsuario.append({
            'sala': res.sala,
            'nombre_recinto': nombre_recinto,
            'fecha_inicio': res.fecha_inicio,
            'hora_inicio': res.hora_inicio,
            'hora_final': res.hora_final,
            'estado': res.estado,
            'comentario': res.comentario
        })

    context = {
        "reservas": reservasUsuario,
        "page_obj": page_obj  # Pasa el objeto de la página actual al template
    }

    return render(request, 'mis_reservas.html', context)
