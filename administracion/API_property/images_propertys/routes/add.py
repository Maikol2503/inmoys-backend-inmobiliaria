import base64
import os
import uuid
from fastapi import APIRouter, HTTPException
from administracion.API_property.images_propertys.schemas.image_request import ImageRequest
from administracion.API_property.models.images_properties_model import Imagen
from config.db import Session

# Crear un router para manejar las propiedades
addImagenProperty = APIRouter()

# Instanciar la sesión de base de datos (esto debe ser manejado en un contexto de dependencias idealmente)
db = Session()

# Directorio principal donde se almacenarán las imágenes
BASE_IMAGE_DIR = "imagenes"
os.makedirs(BASE_IMAGE_DIR, exist_ok=True)

@addImagenProperty.post("/agregar-imagenes-propiedad")
async def addImageProperty(request:dict):
    
    imagenes = request['image']
    id_property: int = request['id_property']

    # # Crear una carpeta para la propiedad usando el id_property
    property_image_dir = os.path.join(BASE_IMAGE_DIR, str(id_property))
    os.makedirs(property_image_dir, exist_ok=True)

    imagenes_guardadas = []

    print(imagenes)

    try:
        for i, base64_image in enumerate(imagenes):
            # Decodificar la imagen en base64
            image_data = base64.b64decode(base64_image['image_name'].split(",")[1])

            # Crear un nombre de archivo único para la imagen
            id_aleatorio = str(uuid.uuid4()).replace('-', '1')[:8]
            image_name = f"image_{id_aleatorio}{id_property}.jpg"
            file_path = os.path.join(property_image_dir, image_name)
            
            # Guardar la imagen en el sistema de archivos
            with open(file_path, "wb") as f:
                f.write(image_data)

            # Crear un registro en la base de datos para la imagen
            nueva_imagen = Imagen(property_id=id_property, image=image_name)
            db.add(nueva_imagen)

            # Hacer flush a la sesión para que se genere el ID
            db.flush()

            # Añadir la imagen guardada a la lista de imágenes guardadas
            imagenes_guardadas.append({
                "id_image": nueva_imagen.id,
                "image_name": nueva_imagen.image
            })

        # Confirmar los cambios en la base de datos
        db.commit()
        # Retornar las imágenes guardadas
        return {"status": "success", "imagenes": imagenes_guardadas}
        
    except Exception as e:
        # Revertir los cambios en caso de error
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
