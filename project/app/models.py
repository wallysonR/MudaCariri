from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser
# Create your models here.



# class User(AbstractUser):
#     pass

class Perfil(models.Model):
    CIDADE_CHOICES = (
        ('juazeiro', 'Juazeiro do Norte'),
        ('crato', 'Crato'),
        ('barbalha', 'Barbalha'),
    )
    rua = models.CharField(null=False, max_length=20)
    cidade = models.CharField(null=False, choices=CIDADE_CHOICES, max_length=20)
    usuario = models.OneToOneField(User, on_delete=models.PROTECT,related_name="perfil")

    def __str__(self):
        return self.usuario.username


class Anuncio(models.Model):
    nome = models.CharField(max_length=20, null=False)
    descricao = models.TextField(max_length=200, null=False)
    data = models.DateTimeField(auto_now=True, null=False)
    foto_capa = models.ImageField(upload_to='media/imagens')
    perfil = models.ForeignKey(Perfil,on_delete=models.CASCADE, default = 0)
    ativo = models.BooleanField(default=True,null=False)
    quantidade = models.IntegerField(default=0, null=False)   
    def __str__(self):
        return self.nome

class Transacao(models.Model):
    STATUS_CHOICES = (
        ('pendente','Pendente'),
        ('aceito','Aceito'),
        ('recusado','Recusado'),
    )
    anuncio = models.ForeignKey(Anuncio,on_delete=models.CASCADE,null= False)
    adotante = models.ForeignKey(Perfil,on_delete=models.CASCADE,null= False)
    quantidade = models.IntegerField(default=1,null= False)
    status = models.CharField(null=False, choices = STATUS_CHOICES,max_length=20)
    def __str__(self):
        return self.anuncio.nome

