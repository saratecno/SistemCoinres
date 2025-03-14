from django.http import HttpResponse
from django.shortcuts import redirect


def auth_users(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard-index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_superuser:  # Permitir acceso sin importar el grupo
                return view_func(request, *args, **kwargs)
            
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name  # Obtiene el primer grupo del usuario
                if group in allowed_roles:
                    return view_func(request, *args, **kwargs)

            return HttpResponse("No tienes permiso para ver esta página.", status=403)  # Código 403: Prohibido
        return wrapper_func
    return decorator