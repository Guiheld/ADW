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
        python 3 manage.py runserver

  Certifique-se que voce possue o framework Django baixado, caso nao, rode o seguinte comando:
       pip install django

    Este projeto foi feito usando o sistema já feito em um trabalho anterior, o seu repositorio é: https://github.com/Guiheld/PythonTrabalhoUemura/tree/v1.0.0. Partes como login, cadastro etc
são reciclados deste sistema.

SOBRE O CODIGO:
    O codigo segue o padrão do framework django, contendo as rotas em urls.py, regras de negocio em views.py e os templates html no diretorio /templates/.
    
    1. Autenticação 
  
      A função de cadastro do sistema utiliza tanto o modelo padrão do Django (User) quanto um modelo personalizado (Usuarios). O modelo padrão do Django é usado para uma implementação rápida e segura, aproveitando as funcionalidades prontas do framework. 
    Por outro lado, o modelo personalizado permite a customização necessária para atender a requisitos específicos do projeto.
    
      Para a função de login, o sistema utiliza exclusivamente o método padrão do Django (login(request, user)). Isso é feito devido à superior segurança e facilidade de implementação oferecidas pelo sistema de autenticação padrão,
    especialmente com relação à automatização do hash de senhas.
    
  Gerenciamento de Tarefas (Criação, Remoção, Edição e Visualização)
  
    2. Visualização
        Após a autenticação, o usuário é redirecionado do login para a função "definir_tarefa", onde são aplicadas as regras de negócios da página "Minhas Tarefas". 
      Nessa função, o sistema busca o objeto do usuário atualmente logado e suas tarefas (aquelas atribuídas a ele, e não as criadas por ele).
      Em seguida, a página HTML é renderizada. Um loop é utilizado para criar um cartão para cada tarefa, listando seus dados. 
      No final do arquivo, há um script em JavaScript que implementa a lógica de filtragem das tarefas com base no seu status/andamento.
      
        A função dashboard pode ser acessada a partir da página "Minhas Tarefas" através de um botão. Nessa função, são buscados todos os usuários e criado um dicionário que mapeia cada usuário para as suas tarefas. 
      Em seguida, a página HTML é renderizada, que é semelhante à página "Minhas Tarefas".

    3. Criação
        A função de criação de tarefas utiliza um formulário definido em formulario.py. Após o usuário preenchê-lo, é criado um objeto de tarefa e o usuário logado é buscado para finalizar a criação da nova tarefa.
      Para criar o formulário, é realizado um query para buscar todos os usuários e uma lista de possiveis valores para "status", o que popula o campo de opções para selecionar o responsável e o status atual da tarefa pela nova tarefa.
      
    4. Exclusão
        A função de exclusão recebe como parâmetro o id da tarefa a ser deletada. Então, a tarefa é buscada e deletada.
      A diferença entre as funções "deletar_tarefa" e "deletar_tarefa_dashboard" é que na função "deletar_tarefa_dashboard" o usuário logado não é buscado.
      
    5. Atualizar/Editar
       A função de editar/atualizar a tarefa foi feita com a lógica semelhante a de exclusão, porém invez de deletar, o usuario é encaminhado para o formulario, onde ele é preenchido novamente e então as alterações são salvas.
      A única diferença entre "atualizar_tarefa" e "atualizar_tarefa_dashboard" também é a mesma que em exclusão, em "atualizar_tarefa_dashboard" não tem uma busca pelo usuario.

Observação: A função "home" serve somente para redirecionar o usuaro à tela de login.
        
  
