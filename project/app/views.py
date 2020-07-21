from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from .models import Perfil, Anuncio, Transacao
from .forms import Perfil,TransacaoForm


class PerfilForm(ModelForm):
    class Meta:
        model = Perfil
        fields = ['rua', 'cidade']


class AnuncioForm(ModelForm):
    class Meta:
        model = Anuncio
        fields = ['nome', 'descricao', 'quantidade']


def home(request, template_name='home.html'):
    return render(request, template_name)


def registrar_usuario(request, template_name="form_usuario.html"):
    form = PerfilForm(request.POST or None)
    if request.method == "POST":
        name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        rua_requesicao = request.POST['rua']
        cidade_requisicao = "juazeiro"
        user = User.objects.create_user(name, email, password)
        user.save()
        perfil = Perfil.objects.create(
            rua=rua_requesicao, cidade=cidade_requisicao, usuario=user)
        perfil.save()
        return redirect('/login')
    return render(request, template_name, {'form': form})


def deletar_usuario(request, pk, template_name="delete.html"):
    perfil = get_object_or_404(Perfil, pk=pk)
    usuario = get_object_or_404(User, id=perfil.usuario_id)
    if request.method == "POST":
        usuario.is_active = False
        usuario.save()
        return HttpResponse("Usuario deletado com sucesso!")
    else:
        return render(request, template_name, {'usuario': usuario})


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


@login_required
def registrar_anuncio(request, template_name="form_anuncio.html"):
    form = AnuncioForm(request.POST or None)
    if request.method == "POST":
        nome_planta = request.POST['nome']
        descricao_planta = request.POST['descricao']
        foto = request.POST['foto']
        qtd = request.POST['quantidade']
        usuario1 = Perfil.objects.get(usuario_id=request.user.id)
        anuncio = Anuncio.objects.create(
            nome=nome_planta, descricao=descricao_planta, foto_capa=foto, perfil=usuario1, quantidade=qtd)
        anuncio.save()
        return redirect('listar_anuncio')
    return render(request, template_name, {'form': form})


@login_required
def listar_anuncio(request, template_name="listar_anuncio.html"):
    anuncios = Anuncio.objects.filter(ativo=True)
    anuncio = {'lista': anuncios}
    return render(request, template_name, anuncio)


@login_required
def listar_anuncio_usuario(request, template_name="listar_anuncio.html"):
    perfil1 = Perfil.objects.get(usuario_id=request.user.id)
    anuncios = Anuncio.objects.filter(perfil=perfil1)
    anuncio = {'lista': anuncios}
    return render(request, template_name, anuncio)


@login_required
def editar_anuncio(request, pk, template_name='form_anuncio.html'):
    anuncio = get_object_or_404(Anuncio, pk=pk)
    if anuncio.ativo == False:
        # TODO mudar para uma subclasse do HTTPRESPONSE
        return HttpResponse('Esse anuncio está desativado')
    else:
        if request.method == "POST":
            form = AnuncioForm(request.POST, instance=anuncio)
            if form.is_valid():
                form.save()
                return redirect('listar_anuncio')
        else:
            form = AnuncioForm(instance=anuncio)
    return render(request, template_name, {'form': form})


@login_required
def deletar_anuncio(request, pk, template_name='delete_anuncio.html'):
    anuncio = get_object_or_404(Anuncio, pk=pk)
    if request.method == "POST":
        anuncio.ativo = False
        anuncio.save()
        return redirect('listar_anuncio')
    return render(request, template_name, {'anuncio': anuncio})


@login_required
def perfil_anuncio(request, pk, template_name='perfil_anuncio.html'):
    anuncio = get_object_or_404(Anuncio, pk=pk)
    return render(request, template_name, {'anuncio': anuncio})


@login_required
def solicitar_transacao(request, pk, template_name='solicitar_item.html'):
    anuncio = get_object_or_404(Anuncio, pk=pk)
    if request.method == 'POST':
        adotante = Perfil.objects.get(usuario_id=request.user.id)
        quantidade_requerida = request.POST['qtd']
        status = 'pendente'
        transacao = Transacao.objects.create(
            anuncio=anuncio, adotante=adotante, quantidade=quantidade_requerida, status=status)
        transacao.save()
        return redirect('listar_anuncio')
    return render(request, template_name, {'anuncio': anuncio})

@login_required
# solicitar transacao 2
def solicitar_transacao2(request,pk,template_name='solicitar_transacao2.html'):
    anuncio = get_object_or_404(Anuncio, pk = pk)
    form = TransacaoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse('Sucesso')
    return render(request, template_name,{'form':form})

def editar_solicitacao(request,pk,template_name='editar_solicitacao.html'):
    transacao = get_object_or_404(Transacao, pk = pk)
    form = TransacaoForm(request.POST or None, instance=transacao)
    if form.is_valid():
        form.save()
        return HttpResponse('Sucesso2')
 
    return render(request,template_name,{'form':form})
@login_required
def listar_transacao(request,template_name='listar_transacao.html'):
    transacoes = Transacao.objects.all()
    transacao = {'lista':transacoes}
    return render(request,template_name,transacao)


@login_required
def minhas_transacoes(request,template_name='listar_transacao.html'):
    perfil1 = Perfil.objects.get(usuario_id=request.user.id)
    anuncios = Anuncio.objects.filter(perfil=perfil1)
    transacoes = Transacao.objects.filter(anuncio__in=anuncios)
    transacao = {'lista':transacoes}
    return render(request,template_name,transacao)


# @login_required
# def mudar_status(request,pk,template_name='mudar_status.html'):
#     transacao = get_object_or_404(Transacao, pk = pk)
#     if request.method == 'POST':

        