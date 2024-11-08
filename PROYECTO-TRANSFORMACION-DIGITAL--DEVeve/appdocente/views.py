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
from .models import Reserva, Reserva2, Recinto,Usuario#, CSVFile  # Import CSVFile model
from .forms import LoginForm , CSVForm  # Import CSVForm
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from appdocente.models import ReporteFrecuencias
from datetime import datetime, timedelta
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .decorators import group_required


# Ocupar landing al momento de hacer logout
def landing(request):
    template = loader.get_template('landing.html')
    return HttpResponse(template.render())

@login_required
def bienvenida(request):
    return render(request, 'bienvenida.html')

def cargarArchivo(request):
    ''
#     my_value = request.session.get('usuario', 'default_value')
#     context = { 'usuarioSesion': my_value }
    form = CSVForm
    return render(request, 'cargarArchivos.html', {'form': form})


def no_autorizado(request):
    return render(request, 'no_autorizado.html')

@login_required
@group_required('encargado')
def listarPeticiones(request):
    correo2 = request.GET.get('correo', '')  # Obtiene el correo desde la URL (parámetro GET)
    
    # Si es una solicitud POST, actualizar el estado de la reserva
    if request.method == 'POST':
        reserva_id = request.POST.get('reserva_id')
        accion = request.POST.get('accion')  # Puede ser 'aprobar' o 'rechazar'
        
        # Obtiene la reserva específica
        reserva = get_object_or_404(Reserva2, id=reserva_id)
        
        if accion == 'aprobar':
            
            #ver si hay conflicto de horario
            conflicto = Reserva2.objects.filter(
            fecha_inicio=reserva.fecha_inicio,
            estado=1, #el 1 es las que estan aprobadas
            recursos=reserva.recursos  #para revisar solo en la misma sala
            ).exclude(id=reserva.id).filter(
                hora_inicio__lt=reserva.hora_fin,  #lt significa menor que
                hora_fin__gt=reserva.hora_inicio   #gt significa mayor que
            ).exists()

            if conflicto:
                
                messages.error(request, "Conflicto de horario: Ya existe una reserva aprobada en este rango de tiempo.")
            else:
                reserva.estado = 1 #con 1 queda reservado
                reserva.save()
                messages.success(request, "Reserva aprobada con éxito.")
        
        elif accion == 'rechazar':
            reserva.estado = 2 #con 2 queda rechazado
            reserva.save()
            messages.success(request, "Reserva rechazada con éxito.")
        

        return redirect('Listar Peticiones')
    
    reservasUsuario = []

    #esto busca por una parte del correo, pero si no se ingresa nada, cargan todos
    reservas = Reserva2.objects.filter(correo__icontains=correo2).order_by('-id') if correo2 else Reserva2.objects.all().order_by('-id')
    
    for res in reservas:
        tipo_recurso = ReporteFrecuencias.objects.filter(recursos=res.recursos).values_list('tipo_recurso', flat=True).first()
        usuario = User.objects.filter(email=res.correo).values_list('first_name', 'last_name').first()
        nombre_completo = f"{usuario[0]} {usuario[1]}" if usuario else "Usuario no encontrado"
        
        reservasUsuario.append({
            'id': res.id,
            'docente': nombre_completo,
            'email': res.correo,
            'recursos': res.recursos,
            'tipo_recurso': tipo_recurso,
            'fecha_inicio': res.fecha_inicio,
            'hora_inicio': res.hora_inicio,
            'hora_final': res.hora_fin,
            'estado': res.estado
        })
    
    context = {"reservas": reservasUsuario, "correo": correo2}
    return render(request, 'listarPeticiones.html', context)

def listarSalas(request):
    return render(request,'listarSalas.html',{'salas':Recinto.objects.all()})

def horarioSala(request):
    #if nombre != None:                  nombre ??? -- de donde viene?
        reservas = Reserva.objects.all()
        context = {'reservas':reservas}

        if reservas:
            return render(request,'horarioSala.html',context) 
        else:
            return render(request,'listarSalas.html',{'mensaje':'Usuario no encontrado'})

class CreateView(generic.edit.CreateView):
    ''
    # model = Reserva
    # fields = ['sala', 'nombre_evento', 'denominacion_evento', 'fecha_inicio', 'hora_inicio', 'hora_fin']
    # def get_form(self):
    #     form = super().get_form()
    #     form.fields['fecha_inicio'].widget = DateTimePickerInput()
    #     return form





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

def listadoDocentes(request):
    if request.method == 'GET':
        docentes = []
        for u in Usuario.objects.all():
            if u.id_cargo.nombre_cargo == 'docente':

                docentes.append({
                    'nombre':u.pnombre + ' ' + u.snombre + ' ' + u.appaterno + ' ' + u.apmaterno,
                    'correo': u.correo
                    })
        context = {"usuarios":docentes}
        return render(request,'ListadoDocentesAdminPage.html',context)
    
    if request.method == 'POST':
        return render(request,'ListadoDocentesAdminPage.html')


# apartado docente 

def homeDocentes(request):
    return render(request,'HomePageDocente.html')

@login_required
@group_required('docente')
def hacerReserva(request):
    
    hoy = datetime.today()

    #calcular semana
    inicio_semana = hoy - timedelta(days=hoy.weekday())  # lunes
    fin_semana = inicio_semana + timedelta(days=5)  # sabado

    #bloques de horas
    bloques_horarios = [
        {"hora_inicio": "08:01", "hora_fin": "08:40"},
        {"hora_inicio": "08:41", "hora_fin": "09:20"},
        {"hora_inicio": "09:31", "hora_fin": "10:10"},
        {"hora_inicio": "10:11", "hora_fin": "10:50"},
        {"hora_inicio": "11:01", "hora_fin": "11:40"},
        {"hora_inicio": "11:41", "hora_fin": "12:20"},
        {"hora_inicio": "12:31", "hora_fin": "13:10"},
        {"hora_inicio": "13:11", "hora_fin": "13:50"},
        {"hora_inicio": "14:01", "hora_fin": "14:40"},
        {"hora_inicio": "14:41", "hora_fin": "15:20"},
        {"hora_inicio": "15:31", "hora_fin": "16:10"},
        {"hora_inicio": "16:11", "hora_fin": "16:50"},
        {"hora_inicio": "17:01", "hora_fin": "17:40"},
        {"hora_inicio": "17:41", "hora_fin": "18:20"},
        {"hora_inicio": "18:21", "hora_fin": "19:00"},
        {"hora_inicio": "19:11", "hora_fin": "19:50"},
        {"hora_inicio": "19:51", "hora_fin": "20:30"},
        {"hora_inicio": "20:41", "hora_fin": "21:20"},
        {"hora_inicio": "21:21", "hora_fin": "22:00"},
        {"hora_inicio": "22:11", "hora_fin": "22:50"},
        {"hora_inicio": "22:51", "hora_fin": "23:30"}
    ]

    #obtener salas
    salasTotales = ReporteFrecuencias.objects.filter(
        recursos__contains="-"
    ).values_list('recursos', flat=True).distinct()
    sala_seleccionada = request.GET.get('sala')

    # Crear una lista de fechas para la semana actual (Lunes a Sábado)
    dias_semana = [(inicio_semana + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6)]

    # Crear un diccionario para almacenar la ocupación de cada bloque horario en cada día
    ocupacion_por_bloque = {}
    for dia in dias_semana:
        ocupacion_por_bloque[dia] = {}
        for bloque in bloques_horarios:
            ocupacion_por_bloque[dia][bloque["hora_inicio"]] = {"estado": "Libre", "fecha": dia}

    if sala_seleccionada:
        # Filtrar las clases de la sala seleccionada para la semana actual
        clases = ReporteFrecuencias.objects.filter(
            recursos=sala_seleccionada,
            fecha_inicio__gte=inicio_semana,
            fecha_inicio__lte=fin_semana
        )

        # Actualizar la ocupación de los bloques de acuerdo a las clases encontradas
        for clase in clases:
            dia_semana = clase.fecha_inicio.strftime('%Y-%m-%d')
            hora_inicio_clase = clase.hora_inicio
            hora_fin_clase = clase.hora_fin

            # Verificar si el día está en dias_semana
            if dia_semana in dias_semana:
                # Marcar todos los bloques que están en el rango de hora_inicio y hora_fin de la clase
                for bloque in bloques_horarios:
                    bloque_inicio = datetime.strptime(bloque["hora_inicio"], "%H:%M").time()
                    bloque_fin = datetime.strptime(bloque["hora_fin"], "%H:%M").time()

                    # Verificar si el bloque está dentro del rango de la clase
                    if (bloque_inicio >= hora_inicio_clase and bloque_inicio < hora_fin_clase) or \
                       (bloque_fin > hora_inicio_clase and bloque_fin <= hora_fin_clase) or \
                       (bloque_inicio <= hora_inicio_clase and bloque_fin >= hora_fin_clase):
                        ocupacion_por_bloque[dia_semana][bloque["hora_inicio"]]["estado"] = "Ocupado"
                        ocupacion_por_bloque[dia_semana][bloque["hora_inicio"]]["fecha"] = dia_semana

    context = {
        "salas": salasTotales,
        "sala_seleccionada": sala_seleccionada,
        "bloques_horarios": bloques_horarios,
        "ocupacion_por_bloque": ocupacion_por_bloque,
        "dias_semana": dias_semana, 
    }


    return render(request, 'HacerReservaDocentePage.html', context)


@login_required
@group_required('docente')
def verReservas(request):
    
    email = request.user.email

    #esto solo se ejcuta si se quiere reservar
    if request.method == 'POST':
        recursos = request.POST.get('recursos')
        fecha = request.POST.get('semana')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        
        print(fecha)
        print(hora_inicio)
        print(hora_fin)
        

        # Crear el nuevo registro de reserva
        Reserva2.objects.create(
            recursos=recursos,
            fecha_inicio=datetime.strptime(fecha, '%Y-%m-%d').date(),
            fecha_final=datetime.strptime(fecha, '%Y-%m-%d').date(),
            hora_inicio=datetime.strptime(hora_inicio, '%H:%M').time(),
            hora_fin=datetime.strptime(hora_fin, '%H:%M').time(),
            correo=email,
            estado=0
        )

        #redirigir para que el codigo de abajo no trabaje
        return redirect('Ver Reservas')

    #si no se registra nada, cargará estp
    reservasUsuario = []
    for res in Reserva2.objects.filter(correo=email).order_by('-id'):
        
        tipo_recurso = ReporteFrecuencias.objects.filter(recursos=res.recursos).values_list('tipo_recurso', flat=True).first()
        
        reservasUsuario.append({
            'recursos': res.recursos,
            'tipo_recurso': tipo_recurso,
            'fecha_inicio': res.fecha_inicio,
            'hora_inicio': res.hora_inicio,
            'hora_final': res.hora_fin,
            'estado': res.estado
        })

    context = {"reservas": reservasUsuario}
    return render(request, 'VerReservasDocentePage.html', context)