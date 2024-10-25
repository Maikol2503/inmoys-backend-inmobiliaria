from typing import List, Optional
from pydantic import BaseModel

class ImagePreview(BaseModel):
    id_image: Optional[str]  # Usar str si el id es un string o puedes usar int si el id es numérico
    image_name: str

class DatosPropiedad(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    documento: Optional[str] = None
    correo: Optional[str] = None
    telefono: Optional[str] = None
    sku: Optional[str] = None
    destacado: Optional[bool] = None
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    provincia: Optional[str] = None
    ciudad: Optional[str] = None
    zona: Optional[str] = None
    puerta: Optional[str] = None
    numeroCalle: Optional[float] = None
    nombreCalle: Optional[str] = None
    planta: Optional[float] = None
    cp: Optional[float] = None
    tipo: Optional[str] = None
    transaccion: Optional[str] = None
    disponibilidad: Optional[str]=None
    detalles: Optional[dict] = None
    image: List[dict] 


    
