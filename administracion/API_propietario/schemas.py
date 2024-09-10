from typing import List, Optional
from pydantic import BaseModel


class DatosPropietario(BaseModel):

    nombre: Optional[str] = None
    apellido: Optional[str] = None
    documento: Optional[str] = None
    correo: Optional[str] = None
    telefono: Optional[str] = None