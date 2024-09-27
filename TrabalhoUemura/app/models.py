from random import choice

from django.contrib.auth.models import User
from django.db import models

# ANOTAÇÕES - Guilherme
# Arquivo responsável por definir os modelos da aplicação. Basicamente, um modelo é -
# a representação das tabelas a serem criadas no banco de dados.

# Create your models here.

from django.db import models

from django.contrib.auth.models import User
from django.db import models

class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=250)
    email = models.EmailField(max_length=250)
    senha = models.CharField(max_length=100)  # ARMAZENAR SENHA EM HASH

    def __str__(self):
        return self.nome


class Tarefas(models.Model):

    Definicao_status = [
        ('pendente', 'Pendente'),
        ('andamento', 'Andamento'),
        ('concluida', 'Concluida'),
    ]

    titulo = models.CharField(max_length=250)
    descricao = models.TextField(max_length=250)
    status = models.CharField(max_length=15, choices=Definicao_status, default='pendente')
    entrada_tarefa = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='nova_tarefa')
    tarefa_atribuida = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True, related_name='atribui_tarefas')

