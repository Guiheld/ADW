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

class analise(models.Model):
    id_analise = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    nome_analise = models.CharField(max_length=100)
    path_arquivo = models.CharField(max_length=100)


def __str__(self):
    return self.nome