import os
from importlib.metadata import files
from traceback import print_exception
from django.contrib.auth.models import User

import csv

from ..models import Usuarios, Livros

backupPrincipal = "principalBackupLivros.csv"
diretorioBackups = os.path.join("app", "backupManager", "LivrosBackupsCSV")
backupTemp = "LivrosBackup"

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



def administradorBackupsTemp(backupTemp):
    files_in_directory = os.listdir(diretorioBackups)
    print(f"Arquivos encontrados: {files_in_directory}")
    files_in_directory = [f for f in files_in_directory if f.startswith(backupTemp) and f.endswith('.csv')]
    print(f"Arquivos filtrados: {files_in_directory}")

    if len(files_in_directory) >= 5:
        oldest_file = sorted(files_in_directory)[0]  # Ordena e pega o mais antigo
        print(f"Removendo o arquivo mais antigo: {oldest_file}")
        os.remove(os.path.join(diretorioBackups, oldest_file))

    num = 0
    while True:
        new_filename = f"{backupTemp}{num}.csv"
        if new_filename not in files_in_directory:
            print(f"Novo arquivo gerado: {new_filename}")
            return new_filename
        num += 1


def deletarLivro(Livros, Usuarios):
    try:
        abs_diretorioBackups = os.path.abspath(diretorioBackups)
        print(f"Diretório absoluto de backups: {abs_diretorioBackups}")

        if not os.path.exists(abs_diretorioBackups):
            print("Diretório de backups temporários de livros não existe.")
            os.makedirs(abs_diretorioBackups)
            print("Diretório criado")
        else:
            print("Diretório existe")

        # Identificar o backup temporário mais recente
        files_in_directory = os.listdir(abs_diretorioBackups)
        files_in_directory = [f for f in files_in_directory if f.startswith(backupTemp) and f.endswith('.csv')]
        if not files_in_directory:
            # Se não houver backups temporários, criar um novo
            latest_backup_file = None
        else:
            # Pegar o mais recente
            latest_backup_file = sorted(files_in_directory, reverse=True)[0]

        # Criar um novo arquivo de backup temporário
        backupTempName = administradorBackupsTemp(backupTemp)
        new_backup_path = os.path.join(abs_diretorioBackups, backupTempName)
        print("Caminho do novo arquivo de backup: " + new_backup_path)

        # Copiar o conteúdo do backup temporário mais recente (se existir) para o novo arquivo de backup
        if latest_backup_file:
            latest_backup_path = os.path.join(abs_diretorioBackups, latest_backup_file)
            print("Copiando do backup mais recente: " + latest_backup_path)
            with open(latest_backup_path, mode='r', newline='', encoding='utf-8') as latest_file:
                reader = csv.reader(latest_file)
                latest_backup_data = list(reader)

            with open(new_backup_path, mode='w', newline='', encoding='utf-8') as new_file:
                writer = csv.writer(new_file)
                for row in latest_backup_data:
                    writer.writerow(row)

        # Adicionar os detalhes do livro deletado ao novo arquivo de backup
        with open(new_backup_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                ['livro_id', 'titulo', 'autor', 'ano_publicacao', 'preco', 'usuarios_donos', 'deletado_por_usuario_id'])
            writer.writerow(
                [Livros.id, Livros.titulo, Livros.autor, Livros.ano_publicacao, Livros.preco, Livros.usuarioDono,
                 Usuarios.id_usuario])
            print(f"Backup atualizado com o livro deletado: {backupTempName}")

    except Exception as e:
        print_exception(type(e), e, e.__traceback__)

#alterar um livro o add em um backup temp, o mais recente, evita muita cria/apaga de arquivos
def alterarLivro(Livros, Usuarios):
    try:
        abs_diretorioBackups = os.path.abspath(diretorioBackups)
        print(f"Diretório absoluto de backups: {abs_diretorioBackups}")

        if not os.path.exists(abs_diretorioBackups):
            print("Diretório de backups temporários de livros não existe.")
            os.makedirs(abs_diretorioBackups)
            print("Diretório criado")
        else:
            print("Diretório existe")

        # Identificar o backup temporário mais recente
        files_in_directory = os.listdir(abs_diretorioBackups)
        files_in_directory = [f for f in files_in_directory if f.startswith(backupTemp) and f.endswith('.csv')]
        if not files_in_directory:
            # Se não houver backups temporários, criar um novo
            backupTempName = administradorBackupsTemp(backupTemp)
        else:
            # Pegar o mais recente
            backupTempName = sorted(files_in_directory, reverse=True)[0]

        file_path = os.path.join(abs_diretorioBackups, backupTempName)
        print("Caminho do diretório: " + file_path)

        # Adicionar os detalhes do livro alterado ao backup temporário existente
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                ['livro_id', 'titulo', 'autor', 'ano_publicacao', 'preco', 'usuarios_donos', 'alterado_por_usuario_id'])
            writer.writerow(
                [Livros.id, Livros.titulo, Livros.autor, Livros.ano_publicacao, Livros.preco, Livros.usuarioDono,
                 Usuarios.id_usuario])
            print(f"Backup alterado: {backupTempName}")

    except Exception as e:
        print_exception(type(e), e, e.__traceback__)

#adiciona um livro importado em um backup temp, o mais recente, evita muita cria/apaga de arquivos
def importLivroTemp(livros_id, titulo, autor, preco, ano_publicacao, usuarioDono, usuario_id, operacao):
    try:
        abs_diretorioBackups = os.path.abspath(diretorioBackups)
        print(f"Diretório absoluto de backups: {abs_diretorioBackups}")

        if not os.path.exists(abs_diretorioBackups):
            print("Diretório de backups temporários de livros não existe.")
            os.makedirs(abs_diretorioBackups)
            print("Diretório criado")
        else:
            print("Diretório existe")

        # Identificar o backup temporário mais recente
        files_in_directory = os.listdir(abs_diretorioBackups)
        files_in_directory = [f for f in files_in_directory if f.startswith(backupTemp) and f.endswith('.csv')]
        if not files_in_directory:
            # Se não houver backups temporários, criar um novo
            backupTempName = administradorBackupsTemp(backupTemp)
        else:
            # Pegar o mais recente
            backupTempName = sorted(files_in_directory, reverse=True)[0]

        file_path = os.path.join(abs_diretorioBackups, backupTempName)
        print("Caminho do diretório: " + file_path)

        # Adicionar os detalhes do livro alterado ao backup temporário existente
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                ['livro_id', 'titulo', 'autor', 'ano_publicacao', 'preco', 'usuarios_donos', operacao])
            writer.writerow(
                [livros_id, titulo, autor, ano_publicacao, preco, usuarioDono,
                 usuario_id])
            print(f"Backup alterado: {backupTempName}")

    except Exception as e:
        print_exception(type(e), e, e.__traceback__)