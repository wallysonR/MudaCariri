from django import forms
from .models import *
from django.contrib.auth.models import User


class PerfilForm(forms.ModelForm):
    rua = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'name': 'rua'}), label="Rua")
    cidade = forms.Select(attrs={'class': 'form-control', 'name': 'cidade'})

    class Meta:
        model = Perfil
        fields = ['rua', 'cidade']

class TransacaoForm(forms.ModelForm):
    class Meta:
        model= Transacao
        fields = ['anuncio','adotante','quantidade','status']