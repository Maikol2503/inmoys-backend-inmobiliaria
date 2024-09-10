from sqlalchemy import Column, Float, String, Table, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Integer
from sqlalchemy.orm import relationship
from config.db import meta, engine, Base

class ClientModel(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100)) 
    apellido = Column(String(100)) 
    documento = Column(String(100)) 
    correo = Column(String(100)) 
    telefono = Column(String(100))
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())
