import logging
from cgi import print_form

import pandas as pd

from .dadosManagerUtils import retirar_coluna_id
from django.conf import settings
import plotly.express as px
from django.shortcuts import render
from plotly.io import to_html

from .graficosOperacoes import separar_e_gerar_graficos


def analisar_dataset(analise_obj):
    logging.info("Iniciando análise para o arquivo: " + analise_obj.nome_analise)
    try:
        df = tranformar_em_dataFrame(analise_obj)
        return df
    except Exception as e:
        logging.error(f"Error reading analise CSV: {str(e)}")
        return None
    # aqui ainda tem que criar a analise por machine learning

def tranformar_em_dataFrame(analise_obj):
    logging.info(f"transformando dataset em dataframe pandas")
    try:
        df = pd.read_csv(analise_obj.path_arquivo, low_memory=False)
        df = retirar_coluna_id(df)
        return df
    except Exception as e:
        logging.error(f"Erro ao tentar transformar o dataset em data frame pandas: {str(e)}")
        return None

# Recebe um data Frame e cria um grafico dependendo do tipo de coluna presente
# param: Data Frame
# return: grafico em html
def criar_grafico(df):
    graficos_html = []
    graficos_html = gerar_lista_graficos_html(graficos_html, df)
    return graficos_html