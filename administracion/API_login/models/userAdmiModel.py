from sqlalchemy import Column, String, Table, Text
from sqlalchemy.sql.sqltypes import Integer
from config.db import meta, engine, Base

class UserAdmiModel(Base):
    __tablename__ = "userAdmi"
    id = Column(Integer, primary_key=True,  autoincrement=True)
    nombre = Column(String(100))
    correo = Column(String(30))
    clave = Column(String(250))
    activo = Column(String(30))
    rol = Column(String(30))
    foto = Column(Text) 
