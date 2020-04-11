from django import forms
from .models import *


class PerfilForm(forms.ModelForm):
    rua = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control','name':'rua'}), label = "Rua")
    cidade = forms.Select(attrs={'class':'form-control','name':'cidade'})

    class Meta:
        model = Perfil
        fields = ['rua','cidade']