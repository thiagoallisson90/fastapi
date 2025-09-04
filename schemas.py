from pydantic import BaseModel
from typing import Optional, List

class UsuarioSchema(BaseModel):
  nome: str
  email: str
  senha: str
  ativo: Optional[bool]
  admin: Optional[bool] = False

  class Config:
    from_attributes = True

class PedidoSchema(BaseModel):
  usuario: int # poderia ser o e-mail e api buscaria o id do usuário no bd

  class Config:
    from_attributes = True


class LoginSchema(BaseModel):
  email: str
  senha: str

  class Config:
    from_attributes = True


class ItemPedidoSchema(BaseModel):
  quantidade: int
  sabor: str
  tamanho: str
  preco_unitario: float

  class Config:
    from_attributes = True

class ResponsePedidoSchema(BaseModel):
  id: int
  status: str
  preco: float
  itens: List[ItemPedidoSchema]

  class Config:
    from_attributes = True