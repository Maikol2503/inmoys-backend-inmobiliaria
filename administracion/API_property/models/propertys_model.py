from sqlalchemy import Boolean, Column, Double, Float, ForeignKey, String, Text, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship
from config.db import Base

class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), unique=True, index=True)
    destacado = Column(Boolean, default=False) 
    descripcion = Column(Text)
    precio = Column(Float)
    tipo = Column(String(100))
    transaccion = Column(String(100))
    provincia = Column(String(100))
    ciudad = Column(String(100))
    zona = Column(String(100))
    cp = Column(Double)
    puerta = Column(String(100))
    planta = Column(Integer)
    numeroCalle = Column(Integer)
    nombreCalle = Column(String(100))
    disponibilidad= Column(String(100))
    detalles = Column(JSON) 
    propietario_id = Column(Integer, ForeignKey('propietario.id'))
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())

  
   