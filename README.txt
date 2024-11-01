Ciencias da Computação - Tópicos Especiais em Software - Professor Marcelo Takashi Uemura

Trabalho 1 - 5
O Sistema de Analise de dados Web (ADW) é capaz de analisar os seguintes datasets:

    Nome do dataset                                Link do kaggle

    sf-salaries -                                  https://www.kaggle.com/datasets/kaggle/sf-salaries/data
    Latest Data Science Job Salaries 2020 - 2024 - https://www.kaggle.com/datasets/saurabhbadole/latest-data-science-job-salaries-2024
    Software Industry Salary Dataset - 2022 -      https://www.kaggle.com/datasets/iamsouravbanerjee/software-professional-salaries-2022

    Os datasets contem informações sobre empregados e empresas e seus salarios e diversas outras informações.
    Os datasets já estão presentes no projeto e no repositorio github.

Integrantes do grupo:
  Guilherme Azevedo Held
  Luciano Moliani

INSTRUÇÕES:

  Certifique-se de baixar as dependencias do projeto
    Django
    Plotly
    numpy

  Após importar o projeto, navegue pelo terminal em sua IDE até o diretório "TrabalhoUemura" e execute os seguintes comandos para a migração:
    Windows:
        1. python manage.py makemigrations
        2. python manage.py migrate
    Linux:
        1. python3 manage.py makemigrations
        2. python3 manage.py migrate

  Em seguida, execute o comando abaixo para rodar o projeto:
    Windows:
        python manage.py runserver
    Linux:
        python3 manage.py runserver

  Este projeto foi feito usando o sistema já feito em um trabalho anterior, o seu repositorio é: https://github.com/Guiheld/gerenciamentoLivraria. Partes como login, cadastro etc são legados deste sistema.
