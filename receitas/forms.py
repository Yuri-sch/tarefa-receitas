from django import forms
from .models import Receita

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['nome', 'descricao', 'custo', 'tipo_receita']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'custo': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_receita': forms.TextInput(attrs={'class': 'form-control'}),
        }