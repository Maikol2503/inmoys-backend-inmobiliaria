from typing import Union, Dict
from fastapi import APIRouter, FastAPI, Depends, HTTPException
from config.db import Session, conn
from passlib.context import CryptContext
from administracion.API_login.models.userAdmiModel import UserAdmiModel
from administracion.API_login.schemas.userAdmi import userAdmiSchema
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt, JWTError
from config.setting import Settings


settings = Settings()
admiLogin = APIRouter()
db = Session()
oauth2_scheme = OAuth2PasswordBearer("/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = settings.secret_key
ALGORIT = "HS256"


def get_user(db, user_email):
    existing_user = db.query(UserAdmiModel).filter(UserAdmiModel.correo == user_email).first()
    if existing_user:
        user = userAdmiSchema.from_orm(existing_user)
        return user.dict() 
    return []

# VERIFICO QUE LAS CONTRASEÑAS SI COINCIDAN
def verify_password(plane_password, hashed_password):
    return pwd_context.verify(plane_password, hashed_password)


def authenticate_user(db, user_email, password):
    user = get_user(db, user_email)
    if not user:
        raise HTTPException(status_code=401, detail="No se pudieron validar las credenciales", headers={"WWW-Authenticate":"Bearer"})
    if not verify_password(password, user["clave"]):
        raise HTTPException(status_code=401, detail="No se pudieron validar las credenciales", headers={"WWW-Authenticate":"Bearer"})
    return user


def create_token(data:dict, time_expires:Union[datetime, None] = None):
    data_copy = data.copy()
    if time_expires is None:
        expires = datetime.utcnow() + timedelta(minutes=15)
    else:
        expires = datetime.utcnow() + time_expires
    data_copy.update({"exp":expires})
    token_jwt = jwt.encode(data_copy, key=SECRET_KEY, algorithm=ALGORIT)
    return token_jwt


def get_user_current(token:str = Depends(oauth2_scheme)):
    print(token)
    try:
        token_decode = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORIT])
        user_correo = token_decode.get("sub")
        if user_correo == None:
            raise HTTPException(status_code=401, detail="No se pudieron validar las credenciales", headers={"WWW-Authenticate":"Bearer"})
    except JWTError:
         raise HTTPException(status_code=401, detail="No se pudieron validar las credenciales", headers={"WWW-Authenticate":"Bearer"})
    user = get_user(db, user_correo)
    if not user :
        raise HTTPException(status_code=401, detail="No se pudieron validar las credenciales", headers={"WWW-Authenticate":"Bearer"})
    return user



def get_user_desable_current(user:userAdmiSchema = Depends(get_user_current)):
    if user["activo"] == "false":
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return user


@admiLogin.get("/users/me")
def userAdmi(user:userAdmiSchema = Depends(get_user_desable_current)):
    return user


@admiLogin.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=30)
    access_token_jwt = create_token({"sub":user["correo"]}, access_token_expires)
    return {
                "access_token":access_token_jwt,
                "token_type":"bearer"

            }
