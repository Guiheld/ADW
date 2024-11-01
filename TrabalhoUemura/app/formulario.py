from django import forms

from .models import analise


class Forms:
    pass

class formulario_nova_analise(forms.ModelForm):
    OPCAO_CHOICES = [
        ('SF_Salaries', 'SF Salaries.csv'),
        ('opcao2', 'Opção 2'),
        ('opcao3', 'Opção 3'),
    ]

    nome_analise = forms.ChoiceField(choices=OPCAO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = analise
        fields = ['nome_analise']