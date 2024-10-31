import logging

import pandas as pd

from .dadosManagerUtils import verificar_header
from django.conf import settings
import plotly.express as px
from django.shortcuts import render
from plotly.io import to_html

from .graficosOperacoes import tentar_criar_graficos


def analisar_dado_completo(analise_obj):
    logging.info("Iniciando análise completa para o arquivo: " + analise_obj.path_arquivo)
    try:
        df = tranformar_em_dataFrame(analise_obj)
        print(df)
        df = df.dropna() # retirna qualquer linha com dado vazio
        return df
    except Exception as e:
        logging.error(f"Error reading analise CSV: {str(e)}")
        return None
    # aqui ainda tem que criar a analise por machine learning



def tranformar_em_dataFrame(dado_importado):
    # Verifica a extensão do arquivo
    if dado_importado.path_arquivo.endswith('.csv'):
        df = pd.read_csv(dado_importado.path_arquivo, low_memory=False)
        return df
    elif dado_importado.path_arquivo.endswith('.tsv'):
        df = pd.read_csv(dado_importado.path_arquivo, delimiter='\t', low_memory=False)
        return df
    elif dado_importado.path_arquivo.endswith('.txt') and verificar_header(dado_importado.path_arquivo, ' '):
        df = pd.read_csv(dado_importado.path_arquivo, delimiter=' ', low_memory=False)
        return df
    elif dado_importado.path_arquivo.endswith('.xlsx'):
        df = pd.read_excel(dado_importado.path_arquivo)
        return df
    elif dado_importado.path_arquivo.endswith('.xls'):
        df = pd.read_excel(dado_importado.path_arquivo)
        return df
    elif dado_importado.path_arquivo.endswith('.json'):
        df = pd.read_json(dado_importado.path_arquivo)
        return df
    elif dado_importado.path_arquivo.endswith('.parquet'):
        df = pd.read_parquet(dado_importado.path_arquivo, low_memory=False)
        return df
    else:
        raise ValueError("Extensão do arquivo não suportada, ou headers nao presentes")


# Recebe um data Frame e cria um grafico dependendo do tipo de coluna presente
# param: Data Frame
# return: grafico em html
def criar_grafico(df):
    graficos_html = []
    graficos_html = tentar_criar_graficos(graficos_html, df)
    return graficos_html