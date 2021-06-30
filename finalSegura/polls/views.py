from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
from polls import models
from django.shortcuts import render, render_to_response
from django.contrib import messages
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .decorators import  login_requerido2
from datetime import timezone
from polls import Cifradores
import logging
import random
import requests
import datetime

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', 
    datefmt='%d-%b-%y %H:%M:%S', 
    level=logging.INFO, filename='bitacora.log', filemode='a+')

def get_client_ip(request):
    """
    Función que recupera la ip del cliente
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def puede_intentar(ip):
    """
    Determina si una ip dada puede volver a intentar enviar el formulario
    La política es 3 intentos máximos por minuto
    La función tiene efectos colaterales en la BD
    La función regresa verdadero o falso
    """
    
    registro_guardado = models.Intentos_por_IP.objects.filter(pk=ip)
    if not registro_guardado:
        registro = models.Intentos_por_IP(ip=ip, contador=1, ultima_petición=datetime.datetime.now())
        registro.save()
        return True
    registro_guardado = registro_guardado[0]
    ahora = datetime.datetime.now(timezone.utc)

    
    ultima = registro_guardado.ultima_petición + datetime.timedelta(hours=5, minutes=1)
    aho = ahora.timestamp()
    ulti = ultima.timestamp()
    if aho > ulti: 
        registro_guardado.ultima_petición = datetime.datetime.now()
        registro_guardado.contador = 1
        registro_guardado.save()
        return True
    else:
        if registro_guardado.contador < 3:
            registro_guardado.ultima_petición = datetime.datetime.now()
            registro_guardado.contador += 1
            registro_guardado.save()
            return True
        else:
            registro_guardado.ultima_petición = datetime.datetime.now()
            return False

def token(request):
    """
    Función que envia el código a telegram
    """
    template='polls/telegram.html'
    if request.method=='GET':
        return render(request, template)
    elif request.method=='POST':
        usuario = request.POST.get('username')
        try:
            user = models.Perfil.objects.get(username=usuario)
            user.TiempoVida = datetime.datetime.now()
            codigoaleatorio0 = random.randint(9999,99999)
            user.CodigoTelegram = codigoaleatorio0
            requests.post('https://api.telegram.org/bot' + user.Token + '/sendMessage', data={'chat_id': user.chatID, 'text': codigoaleatorio0 })
            user.save()
            messages.success(request, f'El codigo ha sido enviado a tu cuenta de telegram.')
            logging.info(f'El código ha sido enviado a tu cuenta de telegram')
            return redirect('login')
        except models.Perfil.DoesNotExist: 
            messages.error(request, f'El usuario no existe.')
            logging.error(f'el usuario no existe')
            return redirect('login')

@login_requerido2
def credenciales_list(request):
    """
    Función que permita listar las credenciales que un usuario ha almacenado
    """
    template = 'polls/credenciales_list2.html'
    if request.method=='GET':
        return render (request,template)
    elif request.method == 'POST':
        cuentas = models.Credenciales.objects.filter(usuario_Asociado_id_id=request.user.id)
        n=0
        for cuenta in cuentas:
            password_cifrador_texto = cuenta.password_cuenta
            password_cifrador = Cifradores.str_bin(password_cifrador_texto)
            iv_inicial=cuenta.iv
            iv_cifrador = Cifradores.str_bin(iv_inicial)
            llave = Cifradores.generar_llave_aes_from_password(request.user.Password_master)
            password_descifrado = Cifradores.descifrar(password_cifrador, llave, iv_cifrador)
            password_texto = password_descifrado.decode('utf-8')
            cuentas[n].password_cuenta = password_texto
            n+=1
        contexto = {'cuentas':cuentas}
        return render(request,template, contexto)

@login_requerido2
def feed(request):
    return render(request, 'polls/feed.html')

@login_requerido2
def registrar_credencial(request):
    """
    Función que le permite a un usuario registrar una credencial
    """
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
        idU = request.user.id
        cuenta.usuario_Asociado_id_id = idU
        
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
    return render(request, template)
    
def acceso(request):
    return render(request, 'polls/acceso.html')

def info(request):
    return render(request, 'polls/info.html')

def fail(request):
    return render(request, 'polls/fail.html')  

    
@login_required
def ingresar(request):
    """
    Función que te solicita el codigo que se envia a telegram para comparar con la BD
    """
    if request.method=='GET':
        return render(request,'polls/token.html')
    if request.method =='POST':
        ip = get_client_ip(request)
        CodigoTelegram = request.POST.get('CodigoTelegram')
        Codigo = request.user.CodigoTelegram
        if not puede_intentar(ip):
            request.session.flush()
            return redirect('fail.html')
        tv = request.user.TiempoVida + datetime.timedelta(hours=5, minutes=2)
        ahora = datetime.datetime.now(timezone.utc)
        aho = ahora.timestamp()
        ulti = tv.timestamp()
        if aho < ulti:
            if CodigoTelegram == Codigo:
                usuario = request.user.username
                user = models.Perfil.objects.get(username=usuario)
                esta = True
                user.is_staff = esta
                user.save()
                return redirect('/')
            else:
                messages.error(request, f'El codigo que ingresaste no es correcto o ha expirado genere otro')
                logging.error(f'El codigo que ingresaste no es correcto o ha expirado genere otro')
                request.session.flush()
                return redirect('login')
        else:
            messages.error(request, f'El codigo que ingresaste no es correcto o ha expirado genere otro')
            logging.error(f'El codigo que ingresaste no es correcto o ha expirado genere otro')
            request.session.flush()
            return redirect('login')


def registro(request):
    """
    Función que permite registrarse a un usuario
    """
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = request.POST.get('password')
            confirmar_password = request.POST.get('confirmar_password')
            master_password = request.POST.get('master_password')
            if password == confirmar_password:
                formulario = form.save()
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
                logging.info(f'Usuario {username} creado')
                return redirect('login')
            else:
                messages.error(request, f'Las contraseña no coinciden')
                logging.error(f'Las contraseña no coinciden')
                return redirect('registro')    
    else:
        form = UserForm()
    context = { 'form' : form }
    return render(request, 'polls/registro.html', context)

@login_requerido2
def logout(request):
    """
    Función para cerrar la sesión de un usuario
    """
    usuario = request.user.username
    user = models.Perfil.objects.get(username=usuario)
    esta = False
    user.is_staff = esta
    leoso = ""
    user.CodigoTelegram = leoso
    user.save()
    messages.info(request, f'Has cerrado sesión.')
    request.session.flush()
    return redirect('/login')