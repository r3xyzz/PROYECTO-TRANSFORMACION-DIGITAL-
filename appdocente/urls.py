from django.urls import path
from . import views
from .views import user_login, user_logout
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('crear_reserva/', views.crear_reserva, name='crear_reserva'),
    path('api/horario/<int:sala_id>/', views.obtener_horario_por_sala, name='obtener_horario_por_sala'),
    path('login/', user_login, name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
