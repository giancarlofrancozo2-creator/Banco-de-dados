# Banco-de-dados
Casa dos Filmes - Sistema de Avaliações
Um sistema interativo via linha de comando (CLI) para gerenciamento de usuários, cadastro de filmes e registro de avaliações, utilizando Python e o ORM SQLAlchemy.

Este projeto foi desenvolvido para praticar conceitos de Banco de Dados Relacional, Relacionamentos entre Tabelas e Operações de CRUD.

 Funcionalidades
Gestão de Usuários: Cadastro com validação de e-mail único e sistema de login.

Catálogo de Filmes: Cadastro de novos títulos com padronização automática (lowercase) para busca facilitada.

Sistema de Avaliações: Usuários logados podem avaliar filmes com notas de 0 a 10 e deixar comentários.

Persistência de Dados: Uso de SQLite para armazenamento local dos dados.

Tecnologias Utilizadas
Python 3

SQLAlchemy (ORM)

SQLite (Banco de Dados)

Estrutura do Banco de Dados
O banco de dados conta com três tabelas principais relacionadas:

Usuarios: Armazena dados de perfil.

Filmes: Armazena informações sobre as obras cinematográficas.

Avaliacoes: Tabela associativa que conecta um Usuário a um Filme, armazenando a nota e o comentário.

Como Executar
Clone o repositório:

Bash
git clone https://github.com/seu-usuario/casa-dos-filmes.git
Instale as dependências:
Este projeto utiliza o SQLAlchemy. Você pode instalá-lo via pip:

Bash
   pip install sqlalchemy
Execute o programa:

Bash
python pyproject.py
