import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Reserva, Sala
from django.http import JsonResponse
from .forms import LoginForm


def obtener_horario_por_sala(request, sala_id):
    # Filtrar las reservas para la sala seleccionada
    reservas = Reserva.objects.filter(sala_id=sala_id).values('fecha_inicio', 'hora_inicio', 'hora_fin', 'nombre_evento')
    return JsonResponse({'reservas': list(reservas)})

@login_required
def index(request):
    # Obtener todas las salas y reservas para mostrarlas en el formulario y horario
    salas = Sala.objects.all()
    reservas = Reserva.objects.all()

    # Serializar las reservas para enviarlas al template
    reservas_json = json.dumps(list(reservas.values('fecha_inicio', 'hora_inicio', 'hora_fin', 'nombre_evento')), cls=DjangoJSONEncoder)

    context = {
        'salas': salas,
        'reservas_json': reservas_json,
    }
    return render(request, 'index.html', context)


def crear_reserva(request):
    salas = Sala.objects.all()
    if request.method == 'POST':
        sala_id = request.POST.get('sala-id')  # Obtener el ID de la sala desde el campo oculto

        # Verifica que el ID de la sala es un número
        if not sala_id.isdigit():
            return JsonResponse({'status': 'error', 'message': 'ID de sala no válido'}, status=400)

        nombre_evento = request.POST.get('nombre-evento')
        descripcion = request.POST.get('descripcion')
        fecha_inicio = request.POST.get('fecha-ini')
        hora_inicio = request.POST.get('hora-inicio')
        hora_fin = request.POST.get('hora-fin')

        # Validar y crear la reserva
        sala = Sala.objects.get(id=int(sala_id))
        reserva = Reserva(
            sala=sala,
            nombre_evento=nombre_evento,
            denominacion_evento=descripcion,
            fecha_inicio=fecha_inicio,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin
        )
        reserva.save()
        return JsonResponse({'status': 'success', 'message': 'Reserva creada exitosamente'})

    context = {
        'salas': salas,
    }
    return render(request, 'index.html', context)

# LOGIN PRINCIPAL (SOLO INICIO DE SESIÓN)
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]  # Extrae el username del email

            # Autenticar usuario
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirige a la vista index.html si las credenciales son correctas
            else:
                messages.error(request, 'Usuario o contraseña incorrectos. Verifica tus datos e intenta nuevamente.')
        else:
            messages.error(request, "Credenciales no válidas. Revisa el formato del correo institucional.")
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


# CERRAR SESIÓN
def user_logout(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión.')
    return redirect('login')
