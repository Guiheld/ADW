import logging
import plotly.express as px
from django.shortcuts import render
from plotly.io import to_html

# funcoes para reconhecer tipo de dataset/colunas e retornar um grafico html

def tentar_criar_graficos(graficos_html, df):
    graficos_html.append(grafico_salario_por_tempo_admissao(df))
    graficos_html.append(grafico_relacao_numero(df))
    graficos_html.append(grafico_relacao_categoria_objeto(df))
    graficos_html.append(graficos_histograma(df))
    if len(graficos_html) > 0:
        return graficos_html
    else:
        logging.error("Nao foi possivel gerar nenhum grafico")
        return []

def grafico_salario_por_tempo_admissao(df):
    try:
        if 'data_admissao' in df.columns:
            logging.info(f"grafico - DataSet identificado como salario e tempo de admissao / gestao de pessoas")
            fig = px.line(df, x='data_admissao', y='salario', title="Tendência de Salário ao Longo do Tempo")
            graph_html = to_html(fig, full_html=False)
            return graph_html
    except Exception as e:
        logging.error(f"erro funcao grafico_salario_por_tempo_admissao, ao tentar criar grafico: {str(e)}")

def grafico_relacao_numero(df):
    try:
        if df.select_dtypes(include=['number']).shape[1] >= 2:
            logging.info(f"grafico - DataSet identificado como relacao entre numeros")
            num_cols = df.select_dtypes(include=['number']).columns[:2]
            fig = px.scatter(df, x=num_cols[0], y=num_cols[1], title=f"Relação entre {num_cols[0]} e {num_cols[1]}")
            graph_html = to_html(fig, full_html=False)
            return graph_html
    except Exception as e:
        logging.error(f"Erro funcao grafico_relacao_numero, ao tentar criar grafico: {str(e)}")

def grafico_relacao_categoria_objeto(df):
    try:
        if df.select_dtypes(include=['category', 'object']).shape[1] >= 1:
            logging.info(f"grafico - DataSet identificado como relacao entre categoria e objeto")
            cat_col = df.select_dtypes(include=['category', 'object']).columns[0]
            num_col = df.select_dtypes(include=['number']).columns[0]
            fig = px.bar(df, x=cat_col, y=num_col, title=f"{num_col} por {cat_col}")
            graph_html = to_html(fig, full_html=False)
            return graph_html
    except Exception as e:
        logging.error(f"Erro funcao grafico_relacao_categoria_objeto, ao tentar criar grafico: {str(e)}")

def graficos_histograma(df):
    try:
        logging.info(f"grafico - grafico gerado como histograma")
        fig = px.histogram(df, x=df.columns[0], title=f"Distribuição de {df.columns[0]}")
        graph_html = to_html(fig, full_html=False)
        return graph_html
    except Exception as e:
        logging.error(f"Erro funcao graficos_histograma, ao tentar criar graficos: {str(e)}")