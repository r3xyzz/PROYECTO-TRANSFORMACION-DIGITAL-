from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('crear_reserva/', views.crear_reserva, name='crear_reserva'),
    path('api/horario/<int:sala_id>/', views.obtener_horario_por_sala, name='obtener_horario_por_sala'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]