import logging

import pandas as pd

from .dadosManagerUtils import verificar_header


def analisar_dado_completo(analise_obj):
    logging.info("Iniciando análise completa para o arquivo: " + analise_obj.path_arquivo)
    try:
        df = tranformar_em_dataFrame(analise_obj)
    except Exception as e:
        logging.error(f"Error reading analise CSV: {str(e)}")
        return

    ## tenta determinar que tipo de data frame se trata para gerar graficos etc

    # Identifica o tipo de dados com base nas colunas detectadas
    if any(col in df.columns for col in ['nome', 'name', 'cargo', 'departamento']):
        logging.info("Detectado dados de gestão de pessoas")


    elif any(col in df.columns for col in ['valor', 'value', 'preco', 'quantidade']):
        logging.info("Detectado dados numéricos ou financeiros")


    else:
        logging.info("Tipo de dados desconhecido, aplicando análise genérica")


def tranformar_em_dataFrame(dado_importado):
    # Verifica a extensão do arquivo
    if dado_importado.path_arquivo.endswith('.csv'):
        df = pd.read_csv(dado_importado.path_arquivo)
        return df
    elif dado_importado.path_arquivo.endswith('.tsv'):
        df = pd.read_csv(dado_importado.path_arquivo, delimiter='\t')
        return df
    elif dado_importado.path_arquivo.endswith('.txt') and verificar_header(dado_importado.path_arquivo, ' '):
        df = pd.read_csv(dado_importado.path_arquivo, delimiter=' ')
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
        df = pd.read_parquet(dado_importado.path_arquivo)
        return df
    else:
        raise ValueError("Extensão do arquivo não suportada, ou headers nao presentes")
