import base64
import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx
from administracion.API_property.images_propertys.schemas.image_request import ImageRequest
from administracion.API_property.models.images_properties_model import Imagen
from config.db import Session

# Crear un router para manejar las propiedades
getImagenProperty = APIRouter()

# Instanciar la sesión de base de datos (esto debe ser manejado en un contexto de dependencias idealmente)
db = Session()

# URL del servicio cliente
url = 'http://localhost:8000/'


@getImagenProperty.get("/obtener-imagenes-propiedad")
async def get_image_urls(property_id: int):
    try:
        images = db.query(Imagen).filter(Imagen.property_id == property_id).all()
        image_urls = [os.path.join("/images", os.path.basename(image.image)) for image in images]
        return image_urls
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")