# import base64
# import os
# import uuid
# from fastapi import APIRouter, HTTPException
# from administracion.API_property.images_propertys.schemas.image_request import ImageRequest
# from administracion.API_property.models.images_properties_model import Imagen
# from config.db import Session


# # Crear un router para manejar las imágenes de propiedades
# deleteImagenProperty = APIRouter()
# # Instanciar la sesión de base de datos
# db = Session()
# # Directorio donde se guardan las imágenes
# IMAGE_DIR = "imagenes"
# os.makedirs(IMAGE_DIR, exist_ok=True)


# @deleteImagenProperty.delete("/eliminar-imagenes-propiedad/{property_id}")
# async def deleteImageProperty(property_id: int):
#     # Construir la ruta de la carpeta de la propiedad
#     property_image_dir = os.path.join(IMAGE_DIR, str(property_id))
#     # Verificar si la carpeta existe
#     if os.path.exists(property_image_dir) and os.path.isdir(property_image_dir):
#         # Eliminar la carpeta y todo su contenido
#         try:
#             import shutil
#             shutil.rmtree(property_image_dir)
#             return {"message": f"Las imágenes de la propiedad con ID {property_id} han sido eliminadas."}
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"No se pudo eliminar la carpeta: {str(e)}")
#     else:
#         raise HTTPException(status_code=404, detail="La carpeta de imágenes de la propiedad no existe.")

