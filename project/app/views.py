from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.forms import ModelForm
from .models import Perfil
from .forms import *


# Create your views here.

class PerfilForm(ModelForm):
    class Meta:
        model = Perfil
        fields = ['rua','cidade']

def registrar_usuario(request,template_name="registrar.html"):
    form = PerfilForm(request.POST or None)
    if request.method=="POST":
        name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        rua_requesicao = request.POST['rua']
        cidade_requisicao = "juazeiro"
        user = User.objects.create_user(name, email, password)
        user.save()
        perfil = Perfil.objects.create(rua=rua_requesicao,cidade=cidade_requisicao,usuario=user)
        perfil.save()
        return redirect('/listar_usuario/')
    return render(request, template_name, {'form':form})

class AnuncioForm(ModelForm):
    class Meta:
        model = Anuncio
        fields = ['nome','descricao']

def registrar_anuncio(request,template_name="registrar_anuncio.html"):
    form = AnuncioForm(request.POST or None)
    if request.method=="POST":
        nome_planta = request.POST['nome']
        descricao_planta = request.POST['descricao']
        usuario1 = Perfil.objects.get(usuario_id = request.user.id)
        anuncio = Anuncio.objects.create(nome=nome_planta,descricao=descricao_planta,perfil=usuario1)
        anuncio.save()
        return HttpResponse("sucesso !")
    return render(request,template_name,{'form':form})
        


# @login_required
# def registrar_usuario(request, template_name="registrar.html"):
#     user = request.user
#     if user.is_staff:
#         if request.method == "POST":
#             username = request.POST['username']
#             email = request.POST['email']
#             password = request.POST['password']
#             tipo = request.POST['tipo_usuario']
#             if tipo == "administrador":
#                 user = User.objects.create_user(username, email, password)
#                 user.is_staff = True
#                 user.save()
#             else:
#                 user = User.objects.create_user(username, email, password)

#             return redirect('/listar_usuario/')
#     else:
#         messages.error(request, 'Permissão negada.')
#         return redirect('/listar_usuario/')

#     return render(request, template_name, {})


@login_required
def listar_usuario(request, template_name="listar.html"):
    usuarios = User.objects.all()
    usuario = {'lista': usuarios}
    return render(request, template_name, usuario)


def logar_usuario(request, template_name='login.html'):
    # next = request.GET.get('listar_usuario')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(home)
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
            return HttpResponseRedirect(settings.LOGIN_URL)

    return render(request, template_name, {'redirect_to': home})


@login_required
def deletar_usuario(request, pk, template_name='delete.html'):
    user = request.user
    if user.has_perm('user.delete_user'):
        try:
            usuario = User.objects.get(pk=pk)
            if request.method == 'POST':
                usuario.delete()
                return redirect('listar_usuario')
        except:
            messages.error(request, 'Usuario não encontrado')
            return redirect('listar_usuario')
    else:
        messages.error(request, 'Permissão negada')
        return redirect('listar_usuario')
    return render(request, template_name, {'usuario': usuario})


def deslogar(request):
    logout(request)
    return redirect(home)


def home(request, template_name='home.html'):
    return render(request, template_name)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
