"""
Sistema de Avaliação de Filmes - Casa dos Filmes
Desenvolvido para gerenciar usuários, filmes e avaliações usando SQLAlchemy e SQLite.
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, validates

#Config do db
db = create_engine ("sqlite:///casadados.db")
Sessao = sessionmaker(bind=db)
sessao = Sessao()

Base = declarative_base()

#tabelas
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String(100), nullable=False)
    email = Column('email', String(100), nullable=False, unique=True)
    senha = Column('senha', String(100), nullable=False)
    avaliacoes = relationship('Avaliacao', back_populates='usuario')
    

#filmes
class Filme(Base):
    __tablename__ = 'filmes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column('titulo', String(200), nullable=False)
    diretor = Column('diretor', String(100), nullable=False)
    ano_lancamento = Column('ano_lancamento', Integer, nullable=False)
    genero = Column('genero', String(100)  , nullable=False)
    sinopse = Column('sinopse', Text, nullable=False)
    avaliacoes = relationship('Avaliacao', back_populates='filme')
    @validates('titulo', 'genero')
    def force_lowercase(self, key, value):
        if value:
            return value.lower()
        return value
#avaliação até 10
class Avaliacao(Base):
    __tablename__ = 'avaliacoes'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    usuario_id = Column('usuario_id', Integer, ForeignKey('usuarios.id'), nullable=False)
    filme_id = Column('filme_id', Integer, ForeignKey('filmes.id'), nullable=False)
    nota = Column('nota', Integer, nullable=False)
    comentario = Column('comentario', Text(2500))
    usuario = relationship('Usuario', back_populates='avaliacoes')
    filme = relationship('Filme', back_populates='avaliacoes')



Base.metadata.create_all(db)


# pagina para login
usuario_logado = None

print('------------Bem-vindo à Casa dos filmes!------------')
print('1. Login')
print('2. Registrar')
opcao = input('Escolha uma opção: ')
if opcao == '1':
    print('---Login---')
    email = input('Email: ').lower()
    senha = input('Senha: ')
    if email and senha:
        usuario_logado = sessao.query(Usuario).filter_by(email=email, senha=senha).first()
        if usuario_logado:
            print(f'Login bem-sucedido! Bem-vindo, {usuario_logado.nome}!')
        else:
            print('Email ou senha incorretos. Tente novamente.')
        exit()
  
elif opcao == '2': 
    print ('---Registro de novo usuário---')
    nome = input('Nome: ')
    email = input('Email: ').lower()
    senha = input('Senha: ')

    novo_usuario = Usuario(nome=nome, email=email, senha=senha)
    sessao.add(novo_usuario)

    try:
        sessao.commit()
        print('Usuário registrado com sucesso! Faça login para continuar.')
        usuario_logado = novo_usuario
    except Exception as e:
        sessao.rollback()
        print(f'Erro email já registrado. Tente novamente.')
        exit()


#area de login para filmes 
if usuario_logado:
    print('---Área de Avaliação de Filmes---')
    titulo_filme = input('Digite o título do filme que deseja avaliar: ').lower()
    filme = sessao.query(Filme).filter_by(titulo=titulo_filme).first()

    if not filme:
        print('Filme não encontrado. Deseja adicionar um novo filme? (s/n)')
        resposta = input().lower()
        if resposta == 's':
            novo_filme = Filme(
                titulo= input('Título: '),
                diretor=input('Diretor: '),
                ano_lancamento=int(input('Ano de lançamento: ')),
                genero=input('Gênero: '),
                sinopse=input('Sinopse: ')
            )
            sessao.add(novo_filme)
            sessao.commit()
            filme = novo_filme
            print('Filme adicionado com sucesso! Agora você pode avaliá-lo.')
        elif resposta == 'n':
            print('Operação cancelada. Volte para o menu principal.')
            filme = None
#registro de avaliação
print('---Registrar Avaliação---')
deseja_avaliar = input('Deseja avaliar este filme? (s/n): ').lower()
if deseja_avaliar == 's':
    nota = int(input('Nota (0-10): '))
    comentario = input('Comentário: ')
    nova_avaliacao = Avaliacao(usuario_id=usuario_logado.id, filme_id=filme.id, nota=nota, comentario=comentario)
    sessao.add(nova_avaliacao)
    sessao.commit()
    print('Avaliação registrada com sucesso!')
elif deseja_avaliar == 'n':
    print('Avaliação cancelada.')
    exit()

#busca de avaliações
if usuario_logado:
    print('---Buscar Avaliações de um Filme---')
    buscar = input('Deseja buscar avaliações de um filme? (s/n): ').lower()
    if buscar == 's':
        buscar_filme = input('Digite o título do filme para buscar avaliações: ').lower()
        filme_buscado = sessao.query(Filme).filter_by(titulo=buscar_filme).first()
        if filme_buscado:
            print(f'---Avaliações para "{filme_buscado.titulo}"---')
            for avaliacao in filme_buscado.avaliacoes:
                print(f'Usuário: {avaliacao.usuario.nome}, Nota: {avaliacao.nota}, Comentário: {avaliacao.comentario}')
        else:
            print('Filme não encontrado.')
