from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from config.db import Session, conn, engine
from administracion.API_login.schemas.userAdmi import userAdmiSchema
from administracion.API_login.models.userAdmiModel import UserAdmiModel
from cryptography.fernet import Fernet
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext

admiRegister = APIRouter()
key = Fernet.generate_key()
f = Fernet(key)
db = Session()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@admiRegister.post("/register")
def register(user:userAdmiSchema):

    existing_user = db.query(UserAdmiModel).filter(UserAdmiModel.correo == user.correo).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya está registrado")
    
    # Cifrar la contraseña antes de guardarla
    hashed_password = hash_password(user.clave)
    user.clave = hashed_password
    print(user.foto)
    new_user = UserAdmiModel(**user.dict())
    db.add(new_user)
    db.commit()
    db.close()

    return JSONResponse(status_code=201, content={"message": "Se ha registrado un nuevo administrador"})









    # new_user = {
    #                 "id":None,  # O bien omitir si id es autoincrementable
    #                 "nombre": "John Doe",
    #                 "correo": "john.doe@example.com",
    #                 "clave": f.encrypt(b"secure_password").decode("utf-8"),
    #                 "activo": "1"
    #             }

    # result = conn.execute(UserAdmiTable.insert().values(new_user))
    # idNewUser = result.lastrowid
    # # Selecciona el nuevo usuario por ID
    # user_data = conn.execute(UserAdmiTable.select().where(UserAdmiTable.c.id == idNewUser)).first()
    # print(user_data)
    # return {
    #         "me":"ok"
    #         }
  


    #  def agregar_alumno(self, data):
    #     alumno = self.db.query(Alumnos_model).filter(Alumnos_model.id_alumno == data.id_alumno).first()

    #     if alumno:
    #         self.logger.warning('El alumno ya existe con este id')
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ya existe un alumno con este id")

    #     nuevo_alumno = Alumnos_model(**data.dict())
    #     #Le envío el nuevo alumno
    #     self.db.add(nuevo_alumno)
    #     #Hago el commit para que se actualice
    #     self.db.commit()
    #     self.logger.info("Se ha registrado un nuevo alumno")  # Log the event
    #     return JSONResponse(status_code=201, content={"message": "Se ha registrado un nuevo alumno"})