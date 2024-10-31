import logging
import os

import pandas as pd
from django.core.files.storage import FileSystemStorage
from ..models import Usuarios, analise
from django.conf import settings
import plotly.express as px
from django.shortcuts import render
from plotly.io import to_html
import numpy as np

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

def mover_colunas_ano_para_data(df, colunas_numericas, colunas_categoricas, colunas_data):
    """
    Move colunas que representam anos (nome 'year', 'Year' ou 'ano') para a lista de colunas de data.
    Não faz conversão de tipos.
    Deveria, mas o pandas fica muito maluco com essa ideia pelo jeito.. enfim, funcao do diabo
    com certeza outra parte do codigo vai transformar em dateTime antes de chegar na analise de machine learning

    :param df: DataFrame com os dados
    :param colunas_numericas: Lista de colunas numéricas identificadas
    :param colunas_categoricas: Lista de colunas categóricas identificadas
    :param colunas_data: Lista de colunas de datas identificadas
    """
    # Identifica colunas que possam representar anos/datas
    possiveis_colunas_data = [col for col in df.columns if col.lower() in ['year', 'ano']]
    logging.warning(f"coluna que representa ano, fora do datetime format encontrada")

    for coluna in possiveis_colunas_data:
        # Move a coluna para colunas_data se não estiver lá
        if coluna not in colunas_data:
            colunas_data.append(coluna)  # Adiciona à lista de datas
            logging.info(f"Coluna '{coluna}' movida para colunas_data")

        # Remove da lista de colunas numéricas ou categóricas, se aplicável
        if coluna in colunas_numericas:
            print(colunas_numericas)
            colunas_numericas.remove(coluna)
            logging.info(f"Coluna '{coluna}' removida de colunas_numericas")
        if coluna in colunas_categoricas:
            colunas_categoricas.remove(coluna)
            logging.info(f"Coluna '{coluna}' removida de colunas_categoricas")

    return colunas_numericas, colunas_categoricas, colunas_data

