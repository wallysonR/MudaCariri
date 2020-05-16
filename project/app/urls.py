from django.conf.urls import url
from .views import *
from django.urls import include, path
urlpatterns = [
    path('',home,name='home'),
    path('registrar_usuario/', registrar_usuario, name='registrar_usuario'),
    path('login/',logar_usuario,name='login'),
    path('login/',logar_usuario),
    path('deslogar/',deslogar,name="deslogar"),
    path('registrar_anuncio/',registrar_anuncio,name="registrar_anuncio"),
    path('listar_anuncio/',listar_anuncio,name="listar_anuncio"),
    path('editar_anuncio/<int:pk>/',editar_anuncio,name="editar_anuncio"),
    path('deletar_anuncio/<int:pk>/',deletar_anuncio,name="deletar_anuncio")
]