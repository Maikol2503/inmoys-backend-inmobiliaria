from typing import List, Optional
from pydantic import BaseModel


class PropertySchema(BaseModel):
    pass
    # sku: Optional[str] = None
    # titulo: Optional[str] = None
    # descripcion: Optional[str] = None
    # precio: Optional[float] = None
    # planta: Optional[float] = None
    # tipo: Optional[str] = None
    # transaccion: Optional[str] = None
    # habitaciones: Optional[int] = None
    # banos: Optional[int] = None
    # ubicacion: Optional[str] = None
    # orientacion: Optional[str] = None
    # piscina: Optional[bool] = None
    # balcon: Optional[bool] = None
    # terraza: Optional[bool] = None
    # jardin: Optional[bool] = None
    # armarioEmpotrado: Optional[bool] = None
    # anoConstruccion: Optional[int]=None
    # estadoInmueble: Optional[str]=None
    # consumo: Optional[str]=None
    # emisiones: Optional[str]=None
    # combustibleCalefaccion: Optional[str]=None
    # sistemaCalefaccion: Optional[str]=None
    # disponibilidad: Optional[str]=None
    # trastero: Optional[bool] = None
    # garaje: Optional[bool] = None
    # aire: Optional[bool] = None 
    # calefaccion: Optional[bool] = None 
    # gimnasio: Optional[bool] = None
    # planta: Optional[int] = None
    # ascensor: Optional[bool] = None
    # tamano: Optional[int] = None  