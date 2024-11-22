# from fastapi import APIRouter, FastAPI, Form, HTTPException
# from fastapi.responses import JSONResponse
# # from administracion.API_propietario.models import PropietarioModel
# # from administracion.API_propietario.schemas import DatosPropietario
# from config.db import Session, conn, engine

# from sqlalchemy.exc import SQLAlchemyError


# from fastapi import FastAPI, HTTPException, Depends


# db = Session()
# addPropietario = APIRouter()

# @addPropietario.post("/agregar-propietario")
# async def create_property(propietario:DatosPropietario):
   
#     new_propietario = PropietarioModel(**propietario.dict())
#     db.add(new_propietario)
#     db.commit()
#     db.refresh(new_propietario)
#     # db.expire_all()
#     return new_propietario
    