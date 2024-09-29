from django import forms
from .models import Livros, Usuarios


class Forms:
    pass

class FormularioDeLivros(forms.ModelForm):
    class Meta:
        model = Livros
        fields = ['titulo', 'autor', 'ano_publicacao', 'preco']
        widgets = {
            'preco': forms.NumberInput(attrs={'step': '0.01'}),
            'ano_publicacao': forms.DateInput(attrs={'type': 'date'}),
        }


