from django.shortcuts import redirect
from functools import wraps
from django.urls import reverse

def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            
            #verificamos permisos
            if request.user.is_authenticated and (request.user.is_superuser or request.user.groups.filter(name=group_name).exists()):
                
                #mostrar vista
                return view_func(request, *args, **kwargs)
            else:
                
                #denegar acceso
                return redirect(reverse('no_autorizado'))
        return _wrapped_view
    return decorator