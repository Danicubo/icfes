from django.shortcuts import redirect

def solo_profesores(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('rol') != 'profesor':
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper