from pydantic import BaseModel
from typing import Optional, Any

class ClientSchema(BaseModel):
    id: Optional[int] = None
    nombre: Optional[str] 
    apellido: Optional[str] 
    documento: Optional[str] 
    correo: Optional[str] 
    telefono: Optional[str] 
   

    class Config:
        orm_mode = True
        