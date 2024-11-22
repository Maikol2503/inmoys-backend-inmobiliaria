# from sqlalchemy import Column, Float, String, Table, Text, DateTime, ForeignKey
# from sqlalchemy.sql import func
# from sqlalchemy.sql.sqltypes import Integer
# from config.db import meta, engine, Base
# from sqlalchemy.orm import relationship

# # class ContratoModel(Base):
# #     __tablename__ = 'contratos'

# #     id = Column(Integer, primary_key=True, index=True)
# #     property_sku = Column(String(100), ForeignKey('properties.sku') )
# #     client_id = Column(Integer, ForeignKey('clientes.id'))
# #     contrato_file = Column(String(100))
# #     fecha_creacion = Column(DateTime, default=func.now())
# #     fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())
