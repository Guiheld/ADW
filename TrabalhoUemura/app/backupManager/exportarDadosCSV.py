from django.http import FileResponse
import os
from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import render
from django.http import FileResponse, Http404, HttpResponse
import os
import zipfile
from io import BytesIO
from django.conf import settings

backupPrincipalLivros = "principalBackupLivros.csv"
backupPrincipalUsuarios = "principalBackupUsuarios.csv"
diretorioBackups = os.path.join("app", "backupManager", "LivrosBackupsCSV")

def download_backup_files(request):
    directory = os.path.dirname(__file__)  # puxa dir que ele esta
    file1_path = os.path.join(directory, backupPrincipalLivros)  # faz o path absoluto

    directory = os.path.dirname(__file__)  # puxa dir que ele esta
    file2_path = os.path.join(directory, backupPrincipalUsuarios)  # faz o path absoluto

    if not (os.path.exists(file1_path) and os.path.exists(file2_path) and os.path.isdir(diretorioBackups)):
        raise Http404("Um ou mais arquivos não foram encontrados")

    # Cria um buffer em memória para o arquivo ZIP
    zip_buffer = BytesIO()

    # Cria um arquivo ZIP
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.write(file1_path, os.path.basename(file1_path))
        zip_file.write(file2_path, os.path.basename(file2_path))
        # backups temporarios
        for filename in os.listdir(diretorioBackups):
            file_path = os.path.join(diretorioBackups, filename)
            if os.path.isfile(file_path):  # Verifica se é um arquivo
                zip_file.write(file_path,
                               os.path.join("LivrosBackupsCSV", filename))  # Mantém a estrutura de diretórios

    # Rewind o buffer
    zip_buffer.seek(0)

    # Retorna o arquivo ZIP como resposta
    response = FileResponse(zip_buffer, as_attachment=True, filename='backup.zip')
    return response