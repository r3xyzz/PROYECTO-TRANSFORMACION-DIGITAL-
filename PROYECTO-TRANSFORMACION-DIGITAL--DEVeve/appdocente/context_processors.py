from django.contrib.auth.models import Group

def grupos_usuario(request):
    es_encargado = False
    es_docente = False
    
    if request.user.is_authenticated:
        # Verifica si el usuario es superadmin
        if request.user.is_superuser:
            es_encargado = True  # Si es superadmin, no es considerado encargado
        else:
            # Comprueba si el usuario pertenece a los grupos específicos
            es_encargado = request.user.groups.filter(name='encargado').exists()
            es_docente = request.user.groups.filter(name='docente').exists()

    return {
        'grupo_encargado': es_encargado,
        'grupo_docente': es_docente,
    }