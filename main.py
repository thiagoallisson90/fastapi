from fastapi import FastAPI
import bcrypt
# https://stackoverflow.com/questions/78628938/trapped-error-reading-bcrypt-version-v-4-1-2
bcrypt.__about__ = bcrypt
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRED_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRED_MINUTES'))

app = FastAPI()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/login-form')

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)