from pydantic import BaseModel
from typing import Optional, Any

class ContratoSchema(BaseModel):
    property_sku: Optional[str] = None
    client_id: Optional[int] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    documento: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    contrato_file: Optional[str] = None
   
    class Config:
        orm_mode = True
        