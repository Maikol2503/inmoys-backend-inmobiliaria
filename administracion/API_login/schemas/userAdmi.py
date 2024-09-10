from pydantic import BaseModel
from typing import Optional, Any

class userAdmiSchema(BaseModel):
    id:Optional[int]
    nombre:str
    correo:str
    clave:str
    activo:str
    rol:str
    foto: Optional[Any]

    class Config:
        orm_mode = True
        from_attributes = True
    
  
