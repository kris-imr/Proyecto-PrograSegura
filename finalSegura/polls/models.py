from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Perfil(AbstractUser):
    Telefono = models.CharField(max_length=30)
    Token = models.CharField(max_length=150)
    chatID = models.CharField(max_length=30)
    CodigoTelegram = models.CharField(max_length=30)
    TiempoVida = models.DateTimeField(null=True)
    salt = models.CharField(max_length=512)
    
class Credenciales(models.Model):
    Nombre_cuenta = models.CharField(max_length=30)
    Usuario_cuenta = models.ForeignKey(Perfil,on_delete=models.CASCADE)
    password_cuenta = models.CharField(max_length=30)
    url_cuenta = models.URLField(max_length=30)
    detalles_cuenta = models.CharField(max_length=100)
    iv = models.CharField(max_length=512)