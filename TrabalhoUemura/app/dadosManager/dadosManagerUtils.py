import logging
import os

from django.core.files.storage import FileSystemStorage


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

#def buscar_path():
