from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', views.feed, name='feed'),
    path('registro/', views.registro, name='registro'),
    path('login/', LoginView.as_view(template_name='polls/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='polls/logout.html'), name='logout'),
    path('token/',views.token,name='token'),
    path('Ingresar/', views.ingresar, name='ingresar'),
    path('credenciales/', views.credenciales, name='credenciales'),
    ]
