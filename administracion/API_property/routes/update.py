import base64
from io import BytesIO
import os
import uuid
from fastapi import APIRouter, HTTPException, Depends, status
from pathlib import Path
import httpx
from administracion.API_property.createData import CreateData
from administracion.API_property.images_propertys.schemas.image_request import ImageRequest
from administracion.API_property.models.images_properties_model import Imagen
from administracion.API_property.models.propertys_model import Property
from administracion.API_property.schemas.data_property_create import DatosPropiedad
from administracion.API_property.schemas.property import PropertySchema
from config.db import Session
from faker import Faker
from io import BytesIO
from PIL import Image

fake = Faker()
updateProperties = APIRouter()
db = Session()
url = 'http://localhost:8000/'

IMAGE_DIR = "imagenes"
os.makedirs(IMAGE_DIR, exist_ok=True)

@updateProperties.put('/editar-propiedad/{property_id}')
async def updatePropertie(property_id:int, property:DatosPropiedad):
    
    # Get the existing property
    existing_property = db.query(Property).filter(Property.id == property_id).first()
    
    if not existing_property:
        raise HTTPException(status_code=404, detail="Property not found")
   
     
    if(property.tipo == 'vivienda'):
        datos_propiedad = CreateData().vivienda(property)
    elif (property.tipo == 'oficina'):
        datos_propiedad = CreateData().oficina(property)
    elif (property.tipo == 'terreno'):
        datos_propiedad = CreateData().terreno(property)

    try:
        propiedad_data_editada = await updateProperty(existing_property, datos_propiedad)
        datos_combinados = {**propiedad_data_editada}
        datos_combinados["id_property"] = property_id
        return datos_combinados
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al editar la propiedad")
    finally:
         db.close()


async def updateProperty(existing_property: Property, data: any):
    try:
        
        if 'destacado' in data:
            existing_property.destacado = data['destacado']
        if 'descripcion' in data:
            existing_property.descripcion = data['descripcion']
        if 'precio' in data:
            existing_property.precio = data['precio']
        if 'tipon' in data:
            existing_property.tipo = data['ubicacion']
        if 'transaccion' in data:
            existing_property.transaccion = data['transaccion']
        if 'disponibilidad' in data:
            existing_property.disponibilidad = data['disponibilidad']
        if 'provincia' in data:
            existing_property.provincia = data['provincia']
        if 'ciudad' in data:
            existing_property.ciudad = data['ciudad']
        if 'zona' in data:
            existing_property.zona = data['zona']
        if 'cp' in data:
            existing_property.cp = data['cp']
        if 'numeroCalle' in data:
            existing_property.numeroCalle = data['numeroCalle']
        if 'nombreCalle' in data:
            existing_property.nombreCalle = data['nombreCalle']  
        if 'planta' in data:
            existing_property.planta = data['planta']  
        if 'puerta' in data:
            existing_property.puerta = data['puerta'] 
        if 'puerta' in data:
            existing_property.puerta = data['puerta']
        if 'detalles' in data:
            existing_property.detalles = data['detalles']
        if 'image' in data:
            existing_property.image = updateImages(data.get('image'), existing_property.sku)
  
        db.commit()
        db.refresh(existing_property)
        # Usar vars() para obtener un diccionario del objeto
        property_dict = vars(existing_property)
        # Filtrar claves internas de SQLAlchemy (que comienzan con "_")
        property_dict = {key: value for key, value in property_dict.items() if not key.startswith('_')}
        return property_dict
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al editar la propiedad")








     
# Para las imágenes nuevas en base64
def updateImages(imagenesList, sku_property_sxisting):
    property_sku = sku_property_sxisting
    imagenes_nuevas = imagenesList[0]['imagenes_nuevas']
    imagenes_guardadas = imagenesList[0]['imagenes_anteriores']
    imagenes_actualizadas = []
    
    
    # Separar las imágenes nuevas (base64) de las imágenes existentes (nombres de archivos)
    # for img in imagenesList:
    #     if img['image'].startswith("data:image"):  # Identificar imágenes nuevas en base64
    #         imagenes_nuevas.append(img)
    #     else:  # Imágenes que ya existían y no se deben eliminar
    #         imagenes_guardadas.append(img)
    
    # subcarpeta_sku = Path(IMAGE_DIR) / property_sku
    
    # # Asegúrate de que la subcarpeta existe antes de iterar
    # if subcarpeta_sku.exists() and subcarpeta_sku.is_dir():
    #     for archivo in subcarpeta_sku.iterdir():
    #         if archivo.is_file():  # Verifica que sea un archivo y no una subcarpeta
    #             if not any(imagen['image'] == archivo.name for imagen in imagenes_guardadas):  # Si no está en las imágenes guardadas, eliminar
    #                 archivo.unlink()  # Eliminar el archivo que no se encuentra en `imagenes_guardadas`
    # for img in imagenesList:
    #     if img['image'].startswith("data:image"):  # Identificar imágenes nuevas en base64
    #         imagenes_nuevas.append(img)
        
    # Ahora guardar las nuevas imágenes base64 en la subcarpeta del SKU
    for img in imagenes_nuevas:
        # Obtener la cadena base64 y separar los metadatos de la imagen
        image_data = img['image'].split(",")[1]  # Separar el prefijo "data:image/png;base64,"
        image_id = img['id']
        image_bytes = base64.b64decode(image_data)  # Decodificar la imagen base64
        id_aleatorio = str(uuid.uuid4()).replace('-', '1')[:8]
        image_name = f"image_{id_aleatorio}{property_sku}.jpg"
        imagenes_actualizadas.append({'id':image_id, 'image':image_name})
       # Crear directorio específico para la propiedad si no existe
        property_dir = os.path.join(IMAGE_DIR, str(property_sku))
        os.makedirs(property_dir, exist_ok=True)
        file_path = os.path.join(property_dir, image_name)
        # Guardar la imagen en el sistema de archivos
        with open(file_path, "wb") as f:
            f.write(image_bytes)
    imagenes_combined = [*imagenes_guardadas, *imagenes_actualizadas]
    return imagenes_combined
  
    
            
    
# en los archivos eliminar las imagenes que no llegaron desde el cliente
# tranformar las imagenes en base 64 y guardarlas en los archivos
#  retornar un array con la imagens que llegaron desde el cliente y las nuevas imagens transormadas



@updateProperties.delete('/eliminar-imagen/{id_imagen}/{sku_property}')
def delete_imagen(id_imagen: str, sku_property: str):
    # Buscar la propiedad en la base de datos usando `sku_property`
    propiedad = db.query(Property).filter(Property.sku == sku_property).first()
    
    # Verificar si la propiedad existe
    if not propiedad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Propiedad no encontrada")

    # Cargar el JSON de imágenes desde la columna `imagenes` (ajusta el nombre si es diferente)
    imagenes = propiedad.image  # Suponiendo que `imagenes` es la columna que almacena el JSON de imágenes
    
    # Buscar la imagen por `id_imagen` en el JSON
    imagen_a_eliminar = next((img for img in imagenes if img.get("id") == id_imagen), None)
    
    # Si la imagen no se encuentra en el JSON, devolver error
    if not imagen_a_eliminar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Imagen no encontrada en la propiedad")

    # Ruta completa a la imagen en el sistema de archivos
    image_name = imagen_a_eliminar["image"]  # Suponiendo que "image" es la clave del nombre de archivo en el JSON
    image_path = Path(IMAGE_DIR) / sku_property / image_name

    # Eliminar la imagen del JSON
    propiedad.image = [img for img in imagenes if img.get("id") != id_imagen]
    
    try:
        # Actualizar la propiedad en la base de datos con el JSON modificado
        db.commit()
        
        # Eliminar el archivo físico de la imagen si existe
        if image_path.exists():
            image_path.unlink()
            print(f"Imagen eliminada del sistema de archivos: {image_path}")

        return {"message": "Imagen eliminada exitosamente"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar la imagen")