from django.conf.urls import url
from .views import *
from django.urls import include, path
urlpatterns = [
    path('login/',logar_usuario),
    path('registrar_usuario/', registrar_usuario, name='registrar_usuario'),
    path('listar_usuario/', listar_usuario, name='listar_usuario'),
    path('login/',logar_usuario,name='login'),
    path("remover_usuario/<int:pk>/",deletar_usuario, name='remover_usuario'),
    path('deslogar/',deslogar,name="deslogar"),
    path('',home,name='home'),
    path('index',index),
    path('registrar_anuncio/',registrar_anuncio,name="registrar_anuncio"),
]