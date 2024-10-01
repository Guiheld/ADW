import csv
import os
import shutil
import sys
import zipfile

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from ..backupManager import backupLivrosCSV
from ..backupManager import backupUsuariosCSV
from ..models import Usuarios, Livros

diretorioSalvar = os.path.join(settings.BASE_DIR, "app", "backupManager", "dadosImportados")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 importarDadosCSV.py <caminho_do_arquivo>")
        sys.exit(1)

def limpar_dir_imports():
    print("bastante log abaixo!!!")
    files_in_directory = os.listdir(diretorioSalvar)
    if len(files_in_directory) > 0:
        print("diretorio de imports está cheio! limpando ...")
        for file in files_in_directory:
            file_path = os.path.join(diretorioSalvar, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                print(f"Arquivo ou diretório {file_path} excluído.")
            except Exception as e:
                print(f"Falha ao deletar {file_path}. Razão: {e}")
        print("diretorio limpado!")

def upload_backup(request):
    if request.method == 'POST' and request.FILES['backup_file']:
        backup_file = request.FILES['backup_file']

        if not backup_file.name.endswith('.zip'):
            print("Erro: arquivo não é um zip!")
            return redirect('dashboard')

        if not os.path.exists(diretorioSalvar):
            print("Diretório de armazenamento de dados importados não existe.")
            os.makedirs(diretorioSalvar)
            print("Diretório criado")
        else:
            print("Diretório de armazenamento de dados importados existe")
            limpar_dir_imports()

        # Salvar o arquivo zip carregado
        fs = FileSystemStorage(location=diretorioSalvar)
        filename = fs.save(backup_file.name, backup_file)
        file_path = os.path.join(diretorioSalvar, filename)

        # Processar o arquivo zip
        process_backup(file_path)

    return redirect('dashboard')


def process_backup(file_path):
    print("arquivo chegou ao processamento, path: " + file_path)

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(diretorioSalvar)

    filepath_principalUsuarios = os.path.join(diretorioSalvar, "principalBackupUsuarios.csv")
    filepath_principalLivros = os.path.join(diretorioSalvar, "principalBackupLivros.csv")
    filepath_LivrosTemp = os.path.join(diretorioSalvar, "LivrosBackupsCSV")

    # log
    if not os.path.exists(filepath_principalUsuarios):
        print("Arquivo de backup danificado, backup principal de usuarios não encontrado!")
    else:
        extrair_usuarios(filepath_principalUsuarios)

    if not os.path.exists(filepath_principalLivros):
        print("Arquivo de backup danificado, backup principal de livros não encontrado!")
    else:
        extrair_livros(filepath_principalLivros)

    if not os.path.exists(filepath_LivrosTemp):
        print("Arquivo de backup danificado, backup temporario de livros não encontrado!")
    else:
        max_file = escolher_backup_temporario(filepath_LivrosTemp)
        extrair_livros_temp(max_file)

def extrair_usuarios(filepath_principalUsuarios):
    try:
        print(f"Diretório absoluto do backup usuarios importado: {filepath_principalUsuarios}")
        usuarios = Usuarios.objects.all()
        num = 0
        with open(filepath_principalUsuarios, mode='r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                usuario_id = row[0]
                nome = row[1]
                email = row[2]
                senha = row[3]
                if not Usuarios.objects.filter(id_usuario=usuario_id).exists() and not Usuarios.objects.filter(nome=nome).exists():
                    user_django = User(username=nome, email=email)
                    Usuarios(nome, email, senha).save()
                    user_django = User(username=nome, email=email)  # cadastra user padrao do django
                    user_django.set_password(senha)
                    user_django.save()
                    num += 1
                    backupUsuariosCSV.atualizaBackupUsuarios()
            print("backup usuarios extraidos do import com sucesso!")
            print("Usuarios únicos adicionados ao banco de dados: " + str(num))
    except Exception as e:
        print(f"erro ao extrair usuarios do backup importado! {e}")

def extrair_livros(filepath_principalLivros):
    try:
        print(f"Diretório absoluto do backup livros importado: {filepath_principalLivros}")
        usuarios = Usuarios.objects.all()
        num = 0
        with open(filepath_principalLivros, mode='r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                livros_id = row[0]
                titulo = row[1]
                email = row[2]
                preco = row[3]
                ano_publicacao = row[4]
                usuarioDono = row[5]
                if not Livros.objects.get(id=livros_id) or not Livros.objects.get(titulo=titulo):
                    Livros(livros_id, titulo, email, preco, ano_publicacao, usuarioDono).save()
                    backupLivrosCSV.atualizaBackupLivros()
            print("backup livros extraidos do import com sucesso!")
            print("livros únicos adicionados ao banco de dados: " + str(num))
    except Exception as e:
        print(f"erro ao extrair livros do backup importado! {e}")

def escolher_backup_temporario(filepath_LivrosTemp):
    try:
        files_in_directory = os.listdir(filepath_LivrosTemp)
        files_in_directory = [f for f in files_in_directory if f.startswith("LivrosBackup") and f.endswith('.csv')]

        if len(files_in_directory) > 0:
            # Encontrar o arquivo com o maior número de linhas
            max_file = max(
                (f for f in files_in_directory),
                key=lambda f: sum(1 for line in open(os.path.join(filepath_LivrosTemp, f))),
                default=None
            )
            if max_file:
                print(f"Arquivo de backup temporário mais completo encontrado: {max_file}")
                max_file = os.path.join(filepath_LivrosTemp + "/" + max_file)
                print(max_file)
                return max_file
            else:
                print("Nenhum arquivo de backup temporário encontrado.")
        else:
            print("Sem backups temporários, ignorando.")
    except Exception as e:
        print(f"Erro ao ler os backups temporários: {e}")


def extrair_livros_temp(max_file):
    try:
        print(f"Diretório absoluto do backup livros temp importado: {max_file}")
        with open(max_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)
            operacao = header[6] + "_importado"
            for row in reader:
                livros_id = row[0]
                titulo = row[1]
                autor = row[2]
                ano_publicacao = row[3]
                preco = row[4]
                usuarioDono = row[5]
                usuario_id = row[6]
                backupLivrosCSV.importLivroTemp(livros_id, titulo, autor, preco, ano_publicacao, usuarioDono, usuario_id, operacao)
            print("backup livros temp extraidos do import com sucesso!")
            print("arquivos temp não são adicionados ao banco de dados")
    except Exception as e:
        print(f"erro ao extrair livros do backup temp importado! {e}")