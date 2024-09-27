from django import forms
from .models import Tarefas, Usuarios


class Forms:
    pass


class Formulario_de_tarefas(forms.ModelForm):
    class Meta:
        modelo = Tarefas
        descricao_tarefas = ['titulo', 'descricao', 'status', 'responsavel_por']
        model = Tarefas
        fields = ['titulo', 'descricao', 'status', 'tarefa_atribuida']
        widgets = {
            'descricao': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'status': forms.Select(choices=[('', 'Selecione o status')] + list(Tarefas.Definicao_status)),
            'tarefa_atribuida': forms.Select(),  # Renderizar como select
        }