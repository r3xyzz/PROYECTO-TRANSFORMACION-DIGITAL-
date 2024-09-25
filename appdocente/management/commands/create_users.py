from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from appdocente.models import UserProfile

class Command(BaseCommand):
    help = 'Crear o actualizar usuarios con sus perfiles de usuario'

    def handle(self, *args, **kwargs):
        users_data = [
            {'username': 'equintana', 'email': 'equintana@duoc.cl', 'password': 'equintanaequintana', 'role': 'Coordinador General Docente'},
            {'username': 'mhenriquez', 'email': 'mhenriquezm@duoc.cl', 'password': 'mhenriquezmhenriquez', 'role': 'Coordinadora Docente'},
            {'username': 'jcampos', 'email': 'jcampos@duoc.cl', 'password': 'jcamposjcampos', 'role': 'Asistente de Coordinación Docente'},
            {'username': 'onunez', 'email': 'onunez@duoc.cl', 'password': 'onunezonunez', 'role': 'Asistente de Coordinación Docente'},
        ]

        for user_data in users_data:
            user, created = User.objects.get_or_create(username=user_data['username'], defaults={'email': user_data['email']})
            if created:
                user.set_password(user_data['password'])
                user.save()

            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = user_data['role']
            profile.save()

            self.stdout.write(self.style.SUCCESS(f"Usuario {user_data['username']} creado/actualizado con rol {user_data['role']}"))
