from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect,get_object_or_404
from django.forms import ModelForm
from .models import Perfil
from .forms import *


# FORMS

class PerfilForm(ModelForm):
    class Meta:
        model = Perfil
        fields = ['rua','cidade']

class AnuncioForm(ModelForm):
    class Meta:
        model = Anuncio
        fields = ['nome','descricao']


#HOME


def home(request, template_name='home.html'):
    return render(request, template_name)


#USUARIO


def registrar_usuario(request,template_name="form_usuario.html"):
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
        return redirect('/login')
    return render(request, template_name, {'form':form})

# TODO EDITAR_USUARIO(PERFIL),EXCLUIR_USUARIO(PERFIL) 

def logar_usuario(request, template_name='login.html'):
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

def deslogar(request):
    logout(request)
    return redirect(home)

 
 
 # ANUNCIO


@login_required
def registrar_anuncio(request,template_name="form_anuncio.html"):
    form = AnuncioForm(request.POST or None)
    if request.method=="POST":
        nome_planta = request.POST['nome']
        descricao_planta = request.POST['descricao']
        usuario1 = Perfil.objects.get(usuario_id = request.user.id)
        anuncio = Anuncio.objects.create(nome=nome_planta,descricao=descricao_planta,perfil=usuario1)
        anuncio.save()
        return redirect('listar_anuncio')
    return render(request,template_name,{'form':form})

@login_required
def listar_anuncio(request, template_name="listar_anuncio.html"):
    anuncios = Anuncio.objects.all()
    anuncio = {'lista':anuncios}
    return render(request,template_name,anuncio)      

@login_required
def editar_anuncio(request,pk ,template_name='form_anuncio.html'):
    anuncio = get_object_or_404(Anuncio, pk=pk)
    if request.method == "POST":
        form = AnuncioForm(request.POST, instance=anuncio)
        if form.is_valid():
            form.save()
            return redirect('listar_anuncio')
    else:
        form = AnuncioForm(instance=anuncio)
    return render(request,template_name,{'form': form})

@login_required
def deletar_anuncio(request,pk, template_name='delete_anuncio.html'):
    anuncio = get_object_or_404(Anuncio, pk=pk)
    if request.method == "POST":
        anuncio.ativo = False
        anuncio.save()
        return redirect('listar_anuncio')
    return render(request,template_name,{'anuncio':anuncio})








