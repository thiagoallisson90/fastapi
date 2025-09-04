from fastapi import APIRouter, Depends, HTTPException
from models import Pedido, Usuario
from schemas import PedidoSchema, ItemPedidoSchema, ResponsePedidoSchema
from dependecies import pegar_sessao, verificar_token
from sqlalchemy.orm import Session
from models import Pedido, ItemPedido
from typing import List

order_router = APIRouter(prefix='/pedidos', tags=['pedidos'], dependencies=[Depends(verificar_token)])

@order_router.get('/')
async def pedidos():
  """
  Essa é a rota padrão de pedidos do nosso sistema.
  Todas as rotas de pedidos precisam de autenticação.
  """
  return {
    'mensagem': 'Você acessou a rota de pedidos'
  }

@order_router.post('/pedido')
async def pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
  novo_pedido = Pedido(usuario=pedido_schema.usuario)
  session.add(novo_pedido)
  session.commit()

  return {
    'mensagem': f'Pedido criado com sucesso! Id do pedido: {novo_pedido.id}'
  }

@order_router.post('/pedido/cancelar/{id_pedido}')
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao),
                          usuario: Usuario = Depends(verificar_token)):
  pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
  if not pedido:
    raise HTTPException(status_code=401, detail='Pedido não encontrado!')

  if not usuario.admin and usuario.id != pedido.usuario:
    raise HTTPException(status_code=401, detail='Você não tem autorização para executar essa operação!')
  
  pedido.status = 'CANCELADO'
  session.commit()

  return {
    'mensagem': f'Pedido {pedido.id} cancelado com sucesso!',
    'pedido': pedido
  }

@order_router.get('/listar')
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
  if not usuario.admin:
    raise HTTPException(status_code=401, detail='Você não tem autorização para fazer essa operação!')
  
  pedidos = session.query(Pedido).all()
  return {
    'pedidos': pedidos,
  }

@order_router.post('/pedido/adicionar-item/{id_pedido}')
async def adicionar_item(id_pedido: int, item_pedido_schema: ItemPedidoSchema, 
                         session: Session = Depends(pegar_sessao), 
                         usuario: Usuario = Depends(verificar_token)):
  pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()

  if not pedido:
    raise HTTPException(status_code=400, detail='Pedido não existente!')
  
  if not usuario.admin and usuario.id != pedido.usuario:
    raise HTTPException(status_code=401, detail='Você não tem autorização para fazer essa operação!')
  
  item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, 
                           item_pedido_schema.tamanho, item_pedido_schema.preco_unitario,
                           id_pedido)
  
  session.add(item_pedido)
  pedido.calcular_preco(item_pedido_schema.preco_unitario * item_pedido_schema.quantidade)
  session.commit()

  return {
    'mensagem': 'Item criado com sucesso!',
    'item_id': item_pedido.id,
    'preco_pedido': pedido.preco
  }

@order_router.post('/pedido/remover-item/{id_item_pedido}')
async def remover_item(id_item_pedido: int, 
                       session: Session = Depends(pegar_sessao), 
                       usuario: Usuario = Depends(verificar_token)):
  item_pedido = session.query(ItemPedido).filter(ItemPedido.id==id_item_pedido).first()

  if not item_pedido:
    raise HTTPException(status_code=400, detail='Pedido não existente!')
  
  pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()
  if not usuario.admin and usuario.id != pedido.usuario:
    raise HTTPException(status_code=401, detail='Você não tem autorização para fazer essa operação!')
  
  preco = item_pedido.preco_unitario * item_pedido.quantidade
  session.delete(item_pedido)
  pedido.calcular_preco(-preco)
  session.commit()

  return {
    'mensagem': f'Item removido com sucesso do pedido {pedido.id}!',
    'qtd_itens': len(pedido.itens),
    'pedido': pedido
  }

@order_router.post('/pedido/finalizar/{id_pedido}')
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao),
                           usuario: Usuario = Depends(verificar_token)):
  pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
  if not pedido:
    raise HTTPException(status_code=401, detail='Pedido não encontrado!')

  if not usuario.admin and usuario.id != pedido.usuario:
    raise HTTPException(status_code=401, detail='Você não tem autorização para executar essa operação!')
  
  pedido.status = 'FINALIZADO'
  session.commit()

  return {
    'mensagem': f'Pedido {pedido.id} finalizado com sucesso!',
    'pedido': pedido
  }

@order_router.get('/pedido/{id_pedido}', response_model=ResponsePedidoSchema)
async def visualizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao),
                           usuario: Usuario = Depends(verificar_token)):
  pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
  if not pedido:
    raise HTTPException(status_code=401, detail='Pedido não encontrado!')

  if not usuario.admin and usuario.id != pedido.usuario:
    raise HTTPException(status_code=401, detail='Você não tem autorização para executar essa operação!')
  
  #return {
  #  'qtd_itens_pedido': len(pedido.itens),
  #  'preco': f'R${pedido.preco:.2f}',
  #  'pedido': pedido
  #}

  return pedido

@order_router.get('/listar/pedidos-usuario', response_model=List[ResponsePedidoSchema])
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)): 
  pedidos = session.query(Pedido).filter(Pedido.usuario==usuario.id).all()
  return pedidos