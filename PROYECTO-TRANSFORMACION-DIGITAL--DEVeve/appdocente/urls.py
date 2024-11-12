from django.urls import path
from . import views
from .views import login

urlpatterns = [
    path('', views.landing, name='Landing'),
    path('no_autorizado', views.no_autorizado, name='no_autorizado'),
    path('bienvenida/', views.bienvenida, name='Bienvenida'),
    path('cargar_archivos/', views.cargarArchivo, name='Cargar Archivos'),
    path('listar_peticiones/', views.listarPeticiones, name='Listar Peticiones'),
    # path('crear_reserva/', views.crear_reserva, name='crear_reserva'),
    # path('api/horario/<int:sala_id>/', views.obtener_horario_por_sala, name='obtener_horario_por_sala'),
    path('login/', login, name='login'),
    path('logout/', views.logout_view, name='logout'),


    path('listadoDocentes/',views.listadoDocentes,name='listado_docentes'),


    path('homeDocentes/',views.homeDocentes,name='home docentes'),
    path('hacerReserva/',views.hacerReserva, name='Hacer reserva'),
    path('verReservas/',views.verReservas,name='Ver Reservas')

]

