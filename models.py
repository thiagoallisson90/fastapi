from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
# from sqlalchemy_utils import ChoiceType

# cria a conexão
db = create_engine('sqlite:///banco.db')

# cria a base do BD
Base = declarative_base()

# cria as classes/tabelas
# Usuario
class Usuario(Base):
  __tablename__ = 'usuarios'

  id = Column('id', Integer, nullable=False, primary_key=True, autoincrement=True)
  nome = Column('nome', String)
  email = Column('email', String, nullable=False, unique=True)
  senha = Column('senha', String)
  ativo = Column('ativo', Boolean, default=True)
  admin = Column('admin', Boolean, default=False)

  def __init__(self, nome, email, senha, ativo=True, admin=False):
    self.nome = nome
    self.email = email
    self.senha = senha
    self.ativo = ativo
    self.admin = admin

# Pedido
class Pedido(Base):
  __tablename__ = 'pedidos'

  #STATUS_PEDIDOS = (
  #  ('PENDENTE', 'PENDENTE'),
  #  ('CANCELADO', 'CANCELADO'),
  #  ('FINALIZADO', 'FINALIZADO')
  #)

  id = Column('id', Integer, nullable=False, primary_key=True, autoincrement=True)
  status = Column('status', String)
  usuario = Column('usuario', ForeignKey('usuarios.id')) 
  preco = Column('preco', Float)
  itens = relationship('ItemPedido', cascade='all, delete')

  def __init__(self, usuario, status='PENDENTE', preco=0):
    self.usuario = usuario
    self.status = status
    self.preco = preco
  
  def calcular_preco(self, preco_pedido: float):
    # self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)
    self.preco += preco_pedido

# ItensPedido
class ItemPedido(Base):
  __tablename__ = 'itens_pedido'

  id = Column('id', Integer, nullable=False, primary_key=True, autoincrement=True)
  quantidade = Column('quantidade', Integer)
  sabor = Column('sabor', String)
  tamanho = Column('tamanho', String)
  preco_unitario = Column('preco_unitario', Float)
  pedido = Column('pedido', ForeignKey('pedidos.id'))

  def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
    self.quantidade = quantidade
    self.sabor = sabor
    self.tamanho = tamanho
    self.preco_unitario = preco_unitario
    self.pedido = pedido

# executa metadados - cria efetivamente o BD