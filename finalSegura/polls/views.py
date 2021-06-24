from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from polls import models
from django.shortcuts import render, render_to_response
from django.contrib import messages
from .forms import UserForm
import random
import requests

# Create your views here.


def token(request):
    template='polls/telegram.html'
    if request.method=='GET':
        return render(request,template)
    elif request.method=='POST':
        usuario = request.POST.get('username')
        user = models.Perfil.objects.get(username=usuario)
        token = user.Token
        chatID = user.chatID
        msj ="Este es tu codigo de acceso, no lo compartas con nadie: "
        codigoAleatorio = random.randint(9999,99999)
        codigoAleatorio2 = str(codigoAleatorio)
        user.CodigoTelegram = codigoAleatorio2
        print (codigoAleatorio2)
        requests.post('https://api.telegram.org/bot' + token + '/sendMessage', data={'chat_id': chatID, 'text': msj+codigoAleatorio2 })
        user.save()
        return redirect('feed')

def feed(request):
    return render(request, 'polls/feed.html')

@login_requerido2
def credenciales(request):
        return render(request, 'polls/upload.html')
    
@login_required
def ingresar(request):
    template = 'polls/token.html'
    if request.method=='GET':
        return render (request,template)
    elif request.method =='POST':
        se = request.session
        print (se)
        CodigoTelegram = request.POST.get('CodigoTelegram')
        Codigo = request.user.CodigoTelegram
        if CodigoTelegram == Codigo:
            return render(request,'polls/acceso.html')
        else:
            request.session.flush()
            return redirect('login')

def registro(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = request.POST.get('password')
            confirmar_password = request.POST.get('confirmar_password')
            if password == confirmar_password:
                formulario = form.save()
                Token = request.POST.get('Token')
                ChatID = request.POST.get('ChatID')
                formulario.set_password(form.cleaned_data['password'])         
                formulario.Token = Token
                formulario.ChatID = ChatID
                formulario.save()
                username = form.cleaned_data['username']
                messages.success(request, f'Usuario {username} creado')
                return redirect('feed')
            else:
                messages.error(request, f'Las contraseña no coinciden')
                return redirect('registro')
    else:
        form = UserForm()
    context = { 'form' : form }
    return render(request, 'polls/registro.html', context)