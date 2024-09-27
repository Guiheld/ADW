from django import forms
from .models import Livros, Usuarios


class Forms:
    pass

class FormularioDeLivros(forms.ModelForm):
    class Meta:
        model = Livros
        fields = ['titulo', 'autor', 'ano_publicacao', 'preco']



