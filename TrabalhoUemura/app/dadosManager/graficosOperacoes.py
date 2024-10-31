import logging
import pandas as pd
import plotly.express as px
from plotly.io import to_html

from .dadosManagerUtils import mover_colunas_ano_para_data


# Função principal para separar e gerar gráficos
def separar_e_gerar_graficos(graficos_html, df):
    logging.info(f"separar_e_gerar_graficos - tentativa de analisar cada coluna e gerar graficos")

    # Separar colunas por tipo
    colunas_numericas = df.select_dtypes(include=['number']).columns.tolist()
    logging.info(f"separar_e_gerar_graficos - " + str(len(colunas_numericas)) + " colunas numericas encontradas")
    colunas_categoricas = df.select_dtypes(include=['category', 'object']).columns.tolist()
    logging.info(f"separar_e_gerar_graficos - " + str(len(colunas_categoricas)) + " colunas categoricas encontradas")
    colunas_data = df.select_dtypes(include=['datetime']).columns
    logging.info(f"separar_e_gerar_graficos - " + str(len(colunas_data)) + " colunas de datas encontradas")

    colunas_numericas, colunas_categoricas, colunas_data = mover_colunas_ano_para_data(df, colunas_numericas, colunas_categoricas, colunas_data)

    # Gerar gráficos para colunas numéricas
    if len(colunas_numericas) >= 2:
        logging.info(f"separar_e_gerar_graficos - gerar graficos numericos")
        graficos_html.append(grafico_relacao_numerica(df, colunas_numericas))
        graficos_html.append(grafico_histograma(df, colunas_numericas))

    # Gerar gráficos para colunas categóricas e numéricas
    if len(colunas_categoricas) >= 1 and len(colunas_numericas) >= 1:
        logging.info(f"separar_e_gerar_graficos - gerar graficos categorias por numeros")
        graficos_html.append(grafico_relacao_categoria_numero(df, colunas_categoricas, colunas_numericas))

    # Gerar gráficos para colunas de datas e numéricas
    if len(colunas_data) >= 1 and len(colunas_numericas) >= 1:
        logging.info(f"separar_e_gerar_graficos - gerar graficos data por numeros")
        graficos_html.append(grafico_tendencia_tempo(df, colunas_data[0], colunas_numericas[0]))

        # Gerar gráfico de proporção entre categorias
    if len(colunas_categoricas) >= 1:
        graficos_html.append(grafico_proporcao_categorias(df, colunas_categoricas[0]))

    return [grafico for grafico in graficos_html if grafico]  # Retorna gráficos válidos


# Função para gerar gráficos de relação numérica
def grafico_relacao_numerica(df, colunas_numericas):
    try:
        logging.info("Gerando gráfico de relação numérica")
        fig = px.line(df, x=colunas_numericas[0], y=colunas_numericas[1],
                      title=f"Relação entre {colunas_numericas[0]} e {colunas_numericas[1]}")
        return to_html(fig, full_html=False)
    except Exception as e:
        logging.error(f"Erro ao criar gráfico de relação numérica: {str(e)}")
        return None


# Função para gerar gráficos de histogramas
def grafico_histograma(df, colunas_numericas):
    try:
        logging.info("Gerando histograma para dados numéricos")
        fig = px.histogram(df, x=colunas_numericas[0], title=f"Distribuição de {colunas_numericas[0]}")
        return to_html(fig, full_html=False)
    except Exception as e:
        logging.error(f"Erro ao criar histograma: {str(e)}")
        return None


# Função para gráficos de relação entre categoria e número
def grafico_relacao_categoria_numero(df, colunas_categoricas, colunas_numericas):
    try:
        logging.info("Gerando gráfico de relação categoria-numérica")
        fig = px.bar(df, x=colunas_categoricas[0], y=colunas_numericas[0],
                     title=f"{colunas_numericas[0]} por {colunas_categoricas[0]}")
        return to_html(fig, full_html=False)
    except Exception as e:
        logging.error(f"Erro ao criar gráfico de relação categoria-numérica: {str(e)}")
        return None


# Função para gráficos de tendência ao longo do tempo
def grafico_tendencia_tempo(df, coluna_data, coluna_numerica):
    try:
        logging.info("Gerando gráfico de tendência ao longo do tempo")
        fig = px.line(df, x=coluna_data, y=coluna_numerica,
                      title=f"Tendência de {coluna_numerica} ao longo de {coluna_data}")
        return to_html(fig, full_html=False)
    except Exception as e:
        logging.error(f"Erro ao criar gráfico de tendência temporal: {str(e)}")
        return None

# Função para gráfico de proporção entre categorias
def grafico_proporcao_categorias(df, coluna_categorica):
    try:
        logging.info("Gerando gráfico de proporção para categorias")
        fig = px.pie(df, names=coluna_categorica, title=f"Proporção de {coluna_categorica}")
        return to_html(fig, full_html=False)
    except Exception as e:
        logging.error(f"Erro ao criar gráfico de proporção de categorias: {str(e)}")
        return None
