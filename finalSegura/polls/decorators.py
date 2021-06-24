from django.shortcuts import render, redirect
from django.http import HttpResponse

def login_requerido2(vista):
    def interna(request, *args, **kwargs):
        if not request.user.username:
            return redirect ('/login')
        return vista(request, *args, **kwargs)
        
    return interna

