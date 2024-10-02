Ciencias da Computação - Tópicos Especiais em Software - Professor Marcelo Takashi Uemura

Trabalho 2 - 0,5
Sistema de Gerenciamento de Livraria Web

Integrantes do grupo:
  Guilherme Azevedo Held
  Luciano Moliani

INSTRUÇÕES:

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

  Certifique-se que voce possue o framework Django baixado, caso nao, rode o seguinte comando:
       pip install django

    Este projeto foi feito usando o sistema já feito em um trabalho anterior, o seu repositorio é: https://github.com/Guiheld/PythonTrabalhoUemura/tree/v1.0.0. Partes como login, cadastro etc são legados deste sistema.

SOBRE O CODIGO:
    O codigo segue o padrão do framework django, contendo as rotas em urls.py, regras de negocio em views.py e os templates html no diretorio /templates/.
    
    1. Autenticação, Visualização, Criação, Exclusão e Atualizar/Editar:
        Funcionam de forma semelhante ao sistema original, com mínimas mudanças para se adaptar ao tema e aos requisitos do trabalho.
  
    2. Backup's Principais
        Para manter a integridade dos dados do banco de dados, foi criado um arquivo CSV que mantém todos os dados que deveriam estar no sistema. Este arquivo é atualizado ao criar, excluir ou editar dados.
      Ele é utilizado tanto para usuários quanto para livros. Se algum cadastro estiver ausente no banco de dados, o sistema o recupera do backup principal.

    3. Backup's Temporarios
        Os backups temporários são criados dinamicamente pelo sistema e gerenciados automaticamente. Caso o diretório não exista, ele é criado dinamicamente. Esses backups não têm utilidade além de permitir a 
      visualização de alterações realizadas pelos usuários ou de dados importados. O sistema permite apenas 5 arquivos temporários, excluindo automaticamente o mais antigo ao criar um novo backup temporário durante
      a exclusão de um livro.
      
    4. Exportação de Backup's
        É possível exportar um backup, gerando um arquivo .zip contendo dois arquivos principais (usuários e livros) e uma pasta com os backups temporários dos livros.
      
    5. Importação de Backup's
       É possível importar um backup, mas ele só será processado se tiver a mesma estrutura do backup gerado pelo próprio sistema. Durante a importação, os dois arquivos principais são processados, e se houver usuários 
      ou livros ausentes no sistema, eles serão adicionados. Quanto aos backups temporários, o conteúdo do arquivo mais recente é inserido no final do backup temporário mais recente do sistema, marcado com a tag "importado" 
      no cabeçalho para indicar a operação realizada.

Observação: Sabemos que o trabalho não precisava ser em django, mas queriamos dar uma caprichada
