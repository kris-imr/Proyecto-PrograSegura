from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Perfil(AbstractUser):
    Telefono = models.CharField(max_length=30)
    Token = models.CharField(max_length=150)
    chatID = models.CharField(max_length=30)
    CodigoTelegram = models.CharField(max_length=30)
    TiempoVida = models.DateTimeField(null=True)
    Password_master = models.CharField(max_length=20)

    
class Credenciales(models.Model):
    Usuario = models.CharField(max_length=30)
    Nombre_cuenta = models.CharField(max_length=30)
    password_cuenta = models.CharField(max_length=30)
    url_cuenta = models.URLField(max_length=30)
    detalles_cuenta = models.CharField(max_length=100)
    iv = models.CharField(max_length=512)
    usuario_Asociado_id=models.ForeignKey(Perfil,on_delete=models.CASCADE)

class Intentos_por_IP(models.Model):
    ip = models.GenericIPAddressField(primary_key=True)
    contador = models.IntegerField(default=0)
    ultima_petición = models.DateTimeField()