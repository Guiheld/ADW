import logging

import pandas as pd


def analisar_dado_completo(analise_obj):
    logging.info("Iniciando análise completa para o arquivo: " + analise_obj.path_arquivo)
    path_arquivo = analise_obj.path_arquivo
    try:
        df = pd.read_csv(path_arquivo)
    except Exception as e:
        logging.error(f"Error reading analise CSV: {str(e)}")
        return

    ## tenta determinar que tipo de data frame se trata para gerar graficos etc

    # Identifica o tipo de dados com base nas colunas detectadas
    if any(col in df.columns for col in ['nome', 'name', 'cargo', 'departamento']):
        logging.info("Detectado dados de gestão de pessoas")
        analisar_gestao_pessoas(df)

    elif any(col in df.columns for col in ['valor', 'value', 'preco', 'quantidade']):
        logging.info("Detectado dados numéricos ou financeiros")
        analisar_dados_numericos(df)

    elif any(col in df.columns for col in ['data', 'date', 'ano', 'mes']):
        logging.info("Detectado dados sobre datas")
        analisar_dados_temporais(df)

    else:
        logging.info("Tipo de dados desconhecido, aplicando análise genérica")
        analise_generica(df)

# Funções de análise específicas

def analisar_gestao_pessoas(df):
    total_funcionarios = df['nome'].nunique() if 'nome' in df.columns else df['name'].nunique()
    cargos = df['cargo'].value_counts() if 'cargo' in df.columns else None
    logging.info(f"Total de funcionários: {total_funcionarios}")
    if cargos is not None:
        logging.info(f"Distribuição de cargos:\n{cargos}")
    # Aqui você pode gerar gráficos específicos para gestão de pessoas

def analisar_dados_numericos(df):
    soma = df['valor'].sum() if 'valor' in df.columns else df['value'].sum()
    media = df['valor'].mean() if 'valor' in df.columns else df['value'].mean()
    logging.info(f"Soma dos valores: {soma}")
    logging.info(f"Média dos valores: {media}")
    # Aqui você pode gerar gráficos como histogramas ou gráficos de barras

def analisar_dados_temporais(df):
    df['data'] = pd.to_datetime(df['data'] if 'data' in df.columns else df['date'], errors='coerce')
    serie_temporal = df.set_index('data').resample('M').size()
    logging.info(f"Série temporal mensal:\n{serie_temporal}")
    # Aqui você pode gerar gráficos de séries temporais, como gráficos de linha

def analise_generica(df):
    logging.info("Resumo dos dados:")
    logging.info(df.describe(include='all'))
    logging.info("Visualização das primeiras linhas do DataFrame:")
    logging.info(df.head())