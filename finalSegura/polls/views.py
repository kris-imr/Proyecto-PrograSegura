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
    template='telegram.html'
    if request.method=='GET':
        return render(request,template)
    elif request.method=='POST':
        username = request.user.username
        try:
            token = request.user.Token
            chatID = request.user.chatID
            codigoAleatorio = random.randint(9999,99999)
            datos_usuario.codigoTelegram = codigoAleatorio
            requests.post('https://api.telegram.org/bot' + token + '/sendMessage', data={'chat_id': chatID, 'text': codigoAleatorio })
            datos_usuario.save()
            return redirect('/')
        except:
            errores={'Ocurrio un error inesperado en APIBOtelegram'}
            return render(request,template,{'errores':errores})



def feed(request):
    return render(request, 'polls/feed.html')

def registro(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            #print (confirmar_password)
            password = request.POST.get('password')
            confirmar_password = request.POST.get('confirmar_password')
            if password == confirmar_password:
                formulario = form.save()
                Telefono = request.POST.get('Telefono')
                Token = request.POST.get('Token')
                ChatID = request.POST.get('ChatID')
                formulario.set_password(form.cleaned_data['password'])         
                formulario.Telefono = Telefono
                formulario.Token = Token
                formulario.ChatID = ChatID
                #formulario.CodigoTelegram = CodigoTelegram
                
                #formulario.set_password(form.cleaned_data['password'])
                formulario.save()
                #print (llave_publica)
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