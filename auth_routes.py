from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import Usuario
from schemas import UsuarioSchema, LoginSchema
from dependecies import pegar_sessao, verificar_token
from main import bcrypt_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRED_MINUTES
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix='/auth', tags=['auth'])

def criar_token(id_usuario: int, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRED_MINUTES)):
  data_expiracao = datetime.now(timezone.utc) \
    + duracao_token
  dict_info = {
    'sub': str(id_usuario), 
    'exp': data_expiracao
  }
  jwt_codificado = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
  return jwt_codificado

def autenticar_usuario(email: str, senha: str, session: Session):
  usuario = session.query(Usuario).filter(Usuario.email==email).first()
  if not usuario:
    return None
  
  if bcrypt_context.verify(senha, usuario.senha):
    return usuario

@auth_router.get('/')
async def home():
  """
  Essa é a rota padrão de autenticação do nosso sistema
  """
  return {
    'mensagem': 'Você acessou a rota padrão de autenticação!', 
    'autenticado': False
  }

@auth_router.post('/criar')
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
  usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()

  if usuario:
    raise HTTPException(status_code=400, detail='E-mail já cadastrado!')
  else:
    senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
    novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada,
                           usuario_schema.ativo, usuario_schema.admin)
    session.add(novo_usuario)
    session.commit()

    return {
      'mensagem': f'Usuário cadastrado com sucesso {usuario_schema.email}.'
    }

# login -> email e senha -> token JWT (JSON Web Token)
@auth_router.post('/login')
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
  usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
  if usuario == None:
    raise HTTPException(status_code=400, 
                        detail='Usuário não encontrado ou credenciais inválidas!')
  else:
    access_token = criar_token(usuario.id)  
    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
    # JWT Bearer
    # headers = {"Access": "Bearer token"}
    return {
      'access_token': access_token,
      'refresh_token': refresh_token,
      'token_type': 'Bearer'
    }

@auth_router.post('/login-form')
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
  usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
  if usuario == None:
    raise HTTPException(status_code=400, 
                        detail='Usuário não encontrado ou credenciais inválidas!')
  else:
    access_token = criar_token(usuario.id)  
    # JWT Bearer
    # headers = {"Access": "Bearer token"}
    return {
      'access_token': access_token,
      'token_type': 'Bearer'
    }

@auth_router.get('/refresh')
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
  access_token = criar_token(usuario.id)
  return {
    'access_token': access_token,
    'token_type': 'Bearer'
  }