import os
from traceback import print_exception
from django.contrib.auth.models import User

import csv

from ..models import Usuarios, Livros

backupPrincipal = "principalBackupLivros.csv"

# Coloca todos Livros que estao no banco de dados no csv backup
def atualizaBackupLivros():
    try:
        directory = os.path.dirname(__file__)  # puxa dir que ele esta
        file_path = os.path.join(directory, backupPrincipal) # faz o path absoluto

        livros = Livros.objects.all()

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['livro_id', 'titulo', 'autor', 'ano_publicacao', 'preco', 'usuarios donos'])

            for livro in livros:
                writer.writerow([livro.id, livro.titulo, livro.autor, livro.ano_publicacao, livro.preco, livro.usuarioDono])
        print(f"Backup feito: {backupPrincipal}")
    except Exception as e:
        print_exception(type(e), e, e.__traceback__)

#percorre o backup principal e verifica se todos os livros estao no banco de dados
def verificaIntegridadeLivros():
    try:
        directory = os.path.dirname(__file__)
        file_path = os.path.join(directory, backupPrincipal)
        if not os.path.exists(file_path):
            print("Arquivo de backup de livros principal nao existe...")
            with open(file_path, 'w') as file:
                file.write("")  # Cria um arquivo vazio
            atualizaBackupLivros()
            print(f"O arquivo {file_path} de backup principal foi criado.")

        usuarios = Usuarios.objects.all()

        with (open(file_path, mode='r', newline='') as file):
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                livros_id = row[0]
                titulo = row[1]

                if not Livros.objects.get(id=livros_id) or not Livros.objects.get(titulo=titulo):
                    print("Banco de dados corrompido: restaurando livros do backup local...")
                    restaurarBancoDeDadosLivros()
                    atualizaBackupLivros()
                    return
    except Exception as e:
        print_exception(type(e), e, e.__traceback__)


def restaurarBancoDeDadosLivros():
    try:
        directory = os.path.dirname(__file__)  # puxa dir que ele esta
        file_path = os.path.join(directory, backupPrincipal)  # faz o path absoluto

        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                livros_id = row[0]
                titulo = row[1]
                email = row[2]
                preco = row[3]
                ano_publicacao = row[4]
                usuarioDono = row[5]
                Livros(livros_id, titulo, email, preco, ano_publicacao,usuarioDono).save()
            print("Banco de dados restaurado com sucesso")

    except Exception as e:
        print_exception(type(e), e, e.__traceback__)