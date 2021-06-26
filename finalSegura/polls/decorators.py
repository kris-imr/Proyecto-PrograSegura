from django.shortcuts import render, redirect

def login_requerido2(vista):
    def interna(request, *args, **kwargs):
        logueado = request.user.is_staff
        if logueado == False:
            request.session.flush()
            return redirect('/login')
        return vista(request, *args, **kwargs)
    return interna

