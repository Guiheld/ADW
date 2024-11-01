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

# Funcao para retirar coluna de id do dataframe pandas
# param: data  frame com coluna de id
# return: data frame sem coluna de id
def retirar_coluna_id(df):
    logging.info("retirando coluna de id do dataframe")
    coluna_id = df.columns[0]
    if pd.api.types.is_integer_dtype(df[coluna_id]) and df[coluna_id].is_unique:
        logging.info(f"coluna que representa o id foi retirada")
        df = df.drop(columns=[coluna_id])
    else:
        logging.info("Nenhuma coluna de ID foi removida.")
    return df

def tranformar_em_dataFrame(analise_obj):
    logging.info(f"transformando dataset em dataframe pandas")
    try:
        df = pd.read_csv(analise_obj.path_arquivo, low_memory=False)
        if analise_obj.nome_analise is 'SF_Salaries':
            df = retirar_coluna_id(df)
        return df
    except Exception as e:
        logging.error(f"Erro ao tentar transformar o dataset em data frame pandas: {str(e)}")
        return None
