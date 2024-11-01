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



    return

# Gráficos de linha que mostram a evolução do salário médio (ou total) ao longo dos anos
# pode ser feito com os dados de BasePay, TotalPay, ou salary_in_usd em função do Year ou work_year.
def salario_por_tempo(graficos_html, df):
    return

# Gráficos de barras que comparam os salários médios por título de trabalho
# pode usar JobTitle ou job_title no eixo X e a média dos salários no eixo Y.
def salario_por_funcao(graficos_html, df):
    return

#  Gráfico de barras que mostra a contagem ou a média de salários por tipo de emprego (e.g., tempo integral, meio período) usando employment_type.
def vagas_por_funcoes(graficos_html, df):
    return

# Gráfico de pizza, Um gráfico que mostra a distribuição de funcionários ativos, inativos, etc., usando Status ou Employment.
def status_por_empregado(graficos_html, df):
    return

# Um gráfico de dispersão que mostra a relação entre salários e o tamanho da empresa (por exemplo, company_size), usando salary e company_size como eixos.
def salario_por_tamanho_da_empresa():
    return