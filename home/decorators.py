from django.http import HttpResponse
from django.shortcuts import redirect, render


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()

            for i in group:
                for x in allowed_roles:
                    if str(i) == str(x):
                        return view_func(request, *args, **kwargs)
            else:
                return render(request, '403.html', status=403)

        return wrapper_func

    return decorator
