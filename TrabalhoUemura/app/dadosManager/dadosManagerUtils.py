import logging
import os

from django.core.files.storage import FileSystemStorage
from ..models import Usuarios, analise
from django.conf import settings

# classe com funcoes frequentemente usadas

def testar_dir_existe_ou_criar(path):
    if not os.path.exists(path):
        logging.info("Diretório de armazenamento de dados importados não existe.")
        os.makedirs(path)
        logging.info("Diretório criado")

# testa se o dir que ele vai salvar o arquivo existe e o salva
def salvar_arquivo_dir_existe(dir_salvar, file):
    testar_dir_existe_ou_criar(dir_salvar)
    fs = FileSystemStorage(location=dir_salvar)
    fs.save(file.name, file)

def verifcar_integridade_banco_de_dados():
    logging.info("Verificando se as analises cadastradas estao importadas localmente")
    try:
        todas_analise = analise.objects.all()
        for analises in todas_analise:
            if not os.path.isfile(analises.path_arquivo):
                logging.warn(f"Arquivo {analises.path_arquivo} não encontrado local, cadastro deletado")
                analises.delete()
    except Exception as e:
        logging.error("e")

# Verifica se o arquivo possui uma header
# param: path do arquivo
# param: delimitador que separa os dados
def verificar_header(path_arquivo, delimiter):
    try:
        # Lê as primeiras linhas do arquivo sem atribuir a um DataFrame
        with open(path_arquivo, 'r') as file:
            first_line = file.readline().strip()
            second_line = file.readline().strip()
        first_line_values = first_line.split(delimiter)
        if second_line:
            second_line_values = second_line.split(delimiter)
            if len(first_line_values) == len(second_line_values):
                return True  # O arquivo tem um cabeçalho
            else:
                return False  # O arquivo não tem um cabeçalho

        return True
    except Exception as e:
        logging.error(f"Erro ao verificar cabeçalho: {str(e)}")
        return False  # Em caso de erro, assume que não há cabeçalho