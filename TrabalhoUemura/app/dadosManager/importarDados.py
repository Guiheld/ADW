import csv
import logging
import os
import shutil
import sys
import zipfile

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from .dadosManagerUtils import testar_dir_existe_ou_criar, salvar_arquivo_dir_existe
from ..models import Usuarios, analise

diretorioSalvar = os.path.join(settings.BASE_DIR, "app", "dadosManager", "dadosImportados")

# Configure the logging
logging.basicConfig(
    level=logging.DEBUG,  # Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato das mensagens de log
    datefmt='%Y-%m-%d %H:%M:%S'  # Formato da data e hora
)

# Funcao para limpar toda a pasta que fica os dados importados pelos usuarios
def limpar_dir_imports():
    logging.info("processo de limpar dir de imports comecando...")
    files_in_directory = os.listdir(diretorioSalvar)
    for file in files_in_directory:
        file_path = os.path.join(diretorioSalvar, file)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            logging.info(f"Arquivo ou diretório {file_path} excluído.")
        except Exception as e:
            logging.error(f"Falha ao deletar {file_path}. Razão: {e}")
    logging.info("diretorio limpado!")

def upload_dados(request):
    if not request.FILES:
        logging.WARN("Nenhum arquivo carregado")
        return redirect('dashboard')
    if request.method == 'POST' and request.FILES:
        for file_key in request.FILES:
            dado_importado = request.FILES[file_key]
            if dado_importado.name.endswith('.csv') or dado_importado.name.endswith('.tsv') or dado_importado.name.endswith('.txt'):
                salvar_arquivo_dir_existe(diretorioSalvar, dado_importado)

                usuario_id = Usuarios.objects.get(id_usuario=request.user.id)
                nome_analise =  dado_importado.name
                path_arquivo = os.path.join(diretorioSalvar, dado_importado.name)
                nova_analise = analise(id_usuario = usuario_id, nome_analise = nome_analise,path_arquivo = path_arquivo)
                nova_analise.save()

                logging.info(f"Arquivo {dado_importado.name} importado com sucesso")
                processar_dados_importado(nova_analise)
            else:
                logging.error(f"Arquivo {dado_importado.name} não é um CSV, TSV ou txt")
                continue
    return redirect('dashboard')

def processar_dados_importado(analise):
    logging.info("arquivo chegou ao processamento, path: " + analise.path_arquivo)

