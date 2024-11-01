import logging
import pandas as pd
import plotly.express as px
from plotly.io import to_html

# ANOTACAO
#   Os datasets possuem alguns headers em comum, entre eles:
#   Salário, Ano, Titulo do Trabalho, Status de Empregado, Agencia ou empresa
#   Entao, para os 3 datasets graficos padroes vao ser gerados, e depois especificos para cada.


# Função principal para separar e gerar gráficos
# param: lista de graficos html
# param: dataframe contendo os dados para gerar os graficos
# return: lista de graficos html completa
def gerar_lista_graficos_html(graficos_html, df):
    graficos_html = salario_por_tempo(graficos_html, df)
    graficos_html = salario_por_funcao(graficos_html, df)
    graficos_html = vagas_por_funcoes(graficos_html, df)
    graficos_html = status_por_empregado(graficos_html, df)
    graficos_html = salario_por_tamanho_da_empresa(graficos_html, df)
    logging.info(f"Graficos gerados: "+str(len(graficos_html)))
    return graficos_html


# Gráficos de linha que mostram a evolução do salário médio (ou total) ao longo dos anos
def salario_por_tempo(graficos_html, df):
    if 'Year' in df.columns or 'work_year' in df.columns:
        ano_coluna = 'Year' if 'Year' in df.columns else 'work_year'
        salario_coluna = 'TotalPay' if 'TotalPay' in df.columns else 'salary_in_usd'

        fig = px.line(df, x=ano_coluna, y=salario_coluna, title='Evolução do Salário ao Longo dos Anos')
        graficos_html.append(to_html(fig, full_html=False))
    return graficos_html


# Gráficos de barras que comparam os salários médios por título de trabalho
def salario_por_funcao(graficos_html, df):
    if 'JobTitle' in df.columns or 'job_title' in df.columns:
        funcao_coluna = 'JobTitle' if 'JobTitle' in df.columns else 'job_title'
        salario_coluna = 'TotalPay' if 'TotalPay' in df.columns else 'salary_in_usd'

        fig = px.bar(df, x=funcao_coluna, y=salario_coluna, title='Salário Médio por Função',
                     labels={funcao_coluna: 'Função', salario_coluna: 'Salário'})
        graficos_html.append(to_html(fig, full_html=False))
    return graficos_html


# Gráfico de barras que mostra a contagem de vagas por tipo de emprego
def vagas_por_funcoes(graficos_html, df):
    if 'employment_type' in df.columns:
        fig = px.bar(df, x='employment_type', title='Contagem de Vagas por Tipo de Emprego')
        graficos_html.append(to_html(fig, full_html=False))
    return graficos_html


# Gráfico de pizza que mostra a distribuição de funcionários ativos, inativos, etc.
def status_por_empregado(graficos_html, df):
    if 'Status' in df.columns or 'Employment' in df.columns:
        status_coluna = 'Status' if 'Status' in df.columns else 'Employment'

        fig = px.pie(df, names=status_coluna, title='Distribuição de Status de Empregados')
        graficos_html.append(to_html(fig, full_html=False))
    return graficos_html


# Gráfico de dispersão que mostra a relação entre salários e o tamanho da empresa
def salario_por_tamanho_da_empresa(graficos_html, df):
    if 'salary' in df.columns and 'company_size' in df.columns:
        fig = px.scatter(df, x='company_size', y='salary', title='Salário por Tamanho da Empresa',
                         labels={'company_size': 'Tamanho da Empresa', 'salary': 'Salário'})
        graficos_html.append(to_html(fig, full_html=False))
    return graficos_html