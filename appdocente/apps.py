from django.apps import AppConfig


class AppdocenteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appdocente'

    def ready(self):
        import appdocente.signals 
