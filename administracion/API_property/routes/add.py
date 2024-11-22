import base64
import os
import uuid
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import httpx
from administracion.API_property.createData import CreateData
# from administracion.API_property.images_propertys.schemas.image_request import ImageRequest
from administracion.API_property.models.propertys_model import Property
from administracion.API_property.schemas.data_property_create import DatosPropiedad
from administracion.API_property.schemas.property import PropertySchema
from config.db import Session
from faker import Faker
import random
import string



fake = Faker()
addProperties = APIRouter()
db = Session()

url = 'http://localhost:8000/'
BASE_IMAGE_DIR = "imagenes"
os.makedirs(BASE_IMAGE_DIR, exist_ok=True)


@addProperties.post("/api/publicar-propiedad/")
async def create_property(property:DatosPropiedad):
     
    if(property.tipo == 'vivienda'):
        datos_propiedad = CreateData().vivienda(property)
    elif (property.tipo == 'oficina'):
        datos_propiedad = CreateData().oficina(property)
    elif (property.tipo == 'terreno'):
        datos_propiedad = CreateData().terreno(property)
    # imagenes = property.image
    try:
        # id_propietario = await addPropietario(datos_propietario)
        id_new_property = await addProperty(datos_propiedad )
        # imagenes_list = await addImagenProperty(id_new_property, imagenes)
        datos_combinados = {**datos_propiedad}
        datos_combinados["id_property"] = id_new_property
        # datos_combinados["image"] = imagenes_list
        return datos_combinados
    except HTTPException as e:      
        raise e
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al crear la propiedad")
    finally:
        db.close()



async def addProperty(data: any):
    try:
        # convertir la imagen de base 64 a una imagen real, 
        # al mismo tiempo se guarda en los archivos
        # save_image_file retorna una lista con los nombres de lasimagenes que se guardaron en los archivos
        imagenes_list = save_image_file(data) 
        data['image'] = imagenes_list
        new_property = Property(**data)
        db.add(new_property)
        db.commit()
        db.refresh(new_property)
        return new_property.id
    except Exception as e:
        # Si ocurre un error, revertir la transacción de la base de datos
        db.rollback()
        # Eliminar las imágenes previamente guardadas en el sistema de archivos
        for image_info in imagenes_list:
            image_path = os.path.join(BASE_IMAGE_DIR, str(data['sku']), image_info['image'])
            if os.path.exists(image_path):
                os.remove(image_path)

        # Loggear el error y lanzar una excepción HTTP
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al crear la propiedad")


def save_image_file(data:any):
    imagenes = data.get('image')
    sku_property = data.get('sku')
    # # # Crear una carpeta para la propiedad usando el id_property
    property_image_dir = os.path.join(BASE_IMAGE_DIR, str(sku_property))
    os.makedirs(property_image_dir, exist_ok=True)
    imagenes_guardadas = []
    try:
        for i, base64_image in enumerate(imagenes):
            # Decodificar la imagen en base64
            image_data = base64.b64decode(base64_image['image'].split(",")[1])
            image_id = base64_image['id']
            # Crear un nombre de archivo único para la imagen
            id_aleatorio = str(uuid.uuid4()).replace('-', '1')[:8]
            image_name = f"image_{id_aleatorio}{i}.jpg"
            file_path = os.path.join(property_image_dir, image_name)
            # Guardar la imagen en el sistema de archivos
            with open(file_path, "wb") as f:
                f.write(image_data)
            imagenes_guardadas.append({'id':image_id , 'image':image_name})
        return imagenes_guardadas
    except Exception as e:
        # Revertir los cambios en caso de error
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
 