import json
import csv
from django.http import JsonResponse, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views import generic
from .models import Reserva, Recinto,Usuario#, CSVFile  # Import CSVFile model
from .forms import LoginForm , CSVForm  # Import CSVForm
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


# Ocupar landing al momento de hacer logout
def landing(request):
    template = loader.get_template('landing.html')
    return HttpResponse(template.render())

def bienvenida(request):
    # usuario = request.session['usuario']
    # context = { 'usuario': usuario }
    template = loader.get_template('bienvenida.html')
    return HttpResponse(template.render())

def cargarArchivo(request):
    ''
#     my_value = request.session.get('usuario', 'default_value')
#     context = { 'usuarioSesion': my_value }
    form = CSVForm
    return render(request, 'cargarArchivos.html', {'form': form})
    
def listarPeticiones(request):
    # # usuario = request.session['usuario']
    # # context = { 'usuario': usuario }
    reservasTotal = []
    for reservas in Reserva.objects.all():
        reservasTotal.append({
                'docente':reservas.id_usuario.correo,
                'sala':reservas.id_recinto.nombre_recinto,
                'asignatura':reservas.id_asignatura.nombre,
                'fecha':reservas.fecha,
                'horaInicio':reservas.hra_inicio,
                'horaFin':reservas.hra_fin,
                'estado':reservas.estado
        })    
    context ={"reservas":reservasTotal}
    return render(request,'listarPeticiones.html',context)



    # template = loader.get_template('listarPeticiones.html')
    # return HttpResponse(template.render())

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
def user_login(request):
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

    return render(request, 'registration/login.html')


#     ''
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
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
def user_logout(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión.')
    return redirect('login')




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

def hacerReserva(request):
    salasTotales = []
    for sala in Recinto.objects.all():
        salasTotales.append(sala.nombre_recinto)
    context={"salas":salasTotales}

    return render(request,'HacerReservaDocentePage.html',context)

def verReservas(request):
    if request.method == 'GET':
        email = request.session["email"]
        reservasUsuario= []
        for res in Reserva.objects.all():
            if res.id_usuario.correo == email:
                reservasUsuario.append({
                    'sala':res.id_recinto.nombre_recinto,
                    'asignatura':res.id_asignatura.nombre,
                    'fecha':res.fecha,
                    'horaInicio':res.hra_inicio,
                    'horaFin':res.hra_fin,
                    'estado':res.estado
                })
        context ={"reservas":reservasUsuario}
        return render(request,'VerReservasDocentePage.html',context)
    else:
        return render(request,'VerReservasDocentePage.html')