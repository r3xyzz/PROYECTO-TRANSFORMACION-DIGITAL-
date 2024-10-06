from django.urls import path
from . import views
from .views import user_login, user_logout

urlpatterns = [
    path('', views.landing, name='Landing'),
    path('bienvenida/', views.bienvenida, name='Bienvenida'),
    path('cargar_archivos/', views.cargarArchivo, name='Cargar Archivos'),
    path('listar_peticiones/', views.listarPeticiones, name='Listar Peticiones'),
    path('listar_salas/', views.listarSalas, name='Listar Salas'),
    path('horario_sala/',views.horarioSala, name='Horario Sala'),
    path('create', views.CreateView.as_view(), name='create'),
    # path('crear_reserva/', views.crear_reserva, name='crear_reserva'),
    # path('api/horario/<int:sala_id>/', views.obtener_horario_por_sala, name='obtener_horario_por_sala'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]

