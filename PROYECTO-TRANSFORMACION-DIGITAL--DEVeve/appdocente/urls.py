from django.urls import path
from . import views
from .views import login

urlpatterns = [
    path('', views.landing, name='Landing'),
    path('no_autorizado', views.no_autorizado, name='no_autorizado'),
    path('bienvenida/', views.bienvenida, name='Bienvenida'),
    path('subir_archivo/', views.subir_archivo, name='subir_archivo'),
    path('reservas/', views.reservas, name='reservas'),
    # path('crear_reserva/', views.crear_reserva, name='crear_reserva'),
    # path('api/horario/<int:sala_id>/', views.obtener_horario_por_sala, name='obtener_horario_por_sala'),
    path('login/', login, name='login'),
    path('logout/', views.logout_view, name='logout'),


    path('docentes/',views.docentes,name='docentes'),


    path('homeDocentes/',views.homeDocentes,name='home docentes'),
    path('reservar/',views.reservar, name='reservar'),
    path('mis_reservas/',views.mis_reservas,name='mis_reservas')

]

