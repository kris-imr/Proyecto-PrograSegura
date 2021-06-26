from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
from polls import models
from django.shortcuts import render, render_to_response
from django.contrib import messages
from .forms import UserForm
import random
import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .decorators import  login_requerido2
from datetime import timezone
import datetime
from polls import Cifradores 


def token(request):
    template='polls/telegram.html'
    if request.method=='GET':
        return render(request,template)
    elif request.method=='POST':
        usuario = request.POST.get('username')
        try:
            user = models.Perfil.objects.get(username=usuario)
            token = user.Token
            chatID = user.chatID
            user.TiempoVida = datetime.datetime.now()
            msj ="Este es tu codigo de acceso, no lo compartas con nadie: "
            codigoAleatorio = random.randint(9999,99999)
            codigoAleatorio2 = str(codigoAleatorio)
            user.CodigoTelegram = codigoAleatorio2
            requests.post('https://api.telegram.org/bot' + token + '/sendMessage', data={'chat_id': chatID, 'text': msj+codigoAleatorio2 })
            user.save()
            messages.success(request, f'El codigo ha sido enviado a tu cuenta de telegram.')
            return redirect('login')
        except:
            messages.error(request, f'El usuario no existe.')
            return redirect('login')

@login_requerido2
def credenciales_list(request):
    template = 'polls/credenciales_list2.html'
    idU = request.user.id
    Password_master = request.user.Password_master
    if request.method=='GET':
        return render (request, template)
    elif request.method == 'POST':
        cuentas = models.Credenciales.objects.filter(usuario_Asociado_id_id=idU)
        n=0
        for cuenta in cuentas:
            Password_master = request.user.Password_master
            password_cifrador_texto = cuenta.password_cuenta
            password_cifrador = Cifradores.str_bin(password_cifrador_texto)
            iv_inicial=cuenta.iv
            iv_cifrador = Cifradores.str_bin(iv_inicial)
            llave = Cifradores.generar_llave_aes_from_password(Password_master)
            password_descifrado = Cifradores.descifrar(password_cifrador, llave, iv_cifrador)
            password_texto = password_descifrado.decode('utf-8')
            cuentas[n].password_cuenta = password_texto
            n+=1
        contexto = {'cuentas':cuentas}
        return render(request,template, contexto)

def feed(request):
    return render(request, 'polls/feed.html')

def registrar_credencial(request):
    template = 'polls/credenciales.html'
    if request.method=='GET':
        return render (request,template)
    if request.method == 'POST':
        username = request.user.username
        Pass_user = request.user.Password_master
        cuenta=models.Credenciales()
        
        Password_master = Pass_user
        Nombre_cuenta = request.POST.get('Nombre_cuenta')
        password_cuenta = request.POST.get('password_cuenta')
        url_cuenta = request.POST.get('url_cuenta')
        detalles_cuenta = request.POST.get('detalles_cuenta')
        
        iv_inicial = Cifradores.generar_iv()
        iv_cifrador = Cifradores.bin_str(iv_inicial)
        llave_aes = Cifradores.generar_llave_aes_from_password(Password_master)
        password_inicial = password_cuenta.encode('utf-8')
        password_cifrador = Cifradores.cifrar(password_inicial, llave_aes, iv_inicial)
        password_cifrador_texto = Cifradores.bin_str(password_cifrador)
    
        cuenta.Usuario = username
        cuenta.Nombre_cuenta = Nombre_cuenta
        cuenta.password_cuenta = password_cifrador_texto
        cuenta.url_cuenta = url_cuenta
        cuenta.detalles_cuenta = detalles_cuenta
        cuenta.iv = iv_cifrador
        cuenta.save()
        return redirect ('/')
    
@login_required
def credenciales(request):
    template=('polls/upload.html')
    if request.method=='GET':
        return render(request, template)
    
@login_required
def ingresar(request):
    template = 'polls/token.html'
    if request.method=='GET':
        return render (request,template)
    elif request.method =='POST':
        CodigoTelegram = request.POST.get('CodigoTelegram')
        Codigo = request.user.CodigoTelegram
        if CodigoTelegram == Codigo:
            return redirect('/')
        else:
            request.session.flush()
            return redirect('login')

def registro(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
       
        if form.is_valid():
            password = request.POST.get('password')
            confirmar_password = request.POST.get('confirmar_password')
            master_password = request.POST.get('master_password')
            if password == confirmar_password:
                formulario = form.save()
                username = request.POST.get('username')
                Telefono = request.POST.get('Telefono')
                Token = request.POST.get('Token')
                ChatID = request.POST.get('ChatID')
                formulario.set_password(form.cleaned_data['password'])         
                formulario.Telefono = Telefono
                formulario.Password_master = Cifradores.generador_clave()
                formulario.Token = Token
                formulario.ChatID = ChatID
                formulario.save()
                username = form.cleaned_data['username']
                messages.success(request, f'Usuario {username} creado')
                return redirect('login')
            else:
                messages.error(request, f'Las contraseña no coinciden')
                return redirect('registro')
            
            
    else:
        form = UserForm()
    context = { 'form' : form }
    return render(request, 'polls/registro.html', context)