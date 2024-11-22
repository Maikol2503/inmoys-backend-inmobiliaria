from sqlite3 import IntegrityError
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import httpx
# from administracion.API_property.models.images_properties_model import Imagen
from administracion.API_property.models.propertys_model import Property
from config.db import Session


# Crear un router para manejar las propiedades
deleteProperties = APIRouter()

# Instanciar la sesión de base de datos (esto debe ser manejado en un contexto de dependencias idealmente)
db = Session()

url =  'http://localhost:8000/'

@deleteProperties.delete("/delete-properties/{property_id}")
async def deletePropeties(property_id:int):
    # Buscar la propiedad en la base de datos
    property_to_delete = db.query(Property).filter(Property.id == property_id).first()
    # Si no se encuentra la propiedad, retornar un error 404
    if property_to_delete is None:
        raise HTTPException(status_code=404, detail="Property not found")
    try:
        # Eliminar la propiedad de la base de datos
        db.delete(property_to_delete)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting property: " + str(e))
    db.expire_all()
    return JSONResponse(content={"message": "Property deleted successfully"}, status_code=200)



