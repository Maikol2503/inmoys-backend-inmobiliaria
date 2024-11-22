# import base64
# import os
# import uuid
# from fastapi import APIRouter, HTTPException
# from administracion.API_property.images_propertys.schemas.image_request import ImageRequest
# from administracion.API_property.models.images_properties_model import Imagen
# from config.db import Session

# # Crear un router para manejar las imágenes de propiedades
# updateImagenProperty = APIRouter()

# # Instanciar la sesión de base de datos
# db = Session()

# # Directorio donde se guardan las imágenes
# IMAGE_DIR = "imagenes"
# os.makedirs(IMAGE_DIR, exist_ok=True)

# @updateImagenProperty.put("/editar-imagenes-propiedad/{property_id}")
# async def editImageProperty(property_id:int, request:ImageRequest):
#     imagenes = request.image  # Imágenes recibidas en la solicitud
#     imagenes_guardadas = []  # Para las imágenes que se mantendrán
#     imagenes_nuevas = []     # Para las imágenes nuevas en base64

#     try:
#         # Separar las imágenes nuevas (base64) de las imágenes existentes (nombres de archivos)
#         for img in imagenes:
#             if img['image_name'].startswith("data:image"):  # Identificar imágenes nuevas en base64
#                 imagenes_nuevas.append(img)
#             else:  # Imágenes que ya existían y no se deben eliminar
#                 imagenes_guardadas.append(img)

#         # Obtener todas las imágenes existentes en la base de datos para la propiedad especificada
#         existing_images = db.query(Imagen).filter(Imagen.property_id == property_id).all()
        
#         # Elimino las imágenes que no están incluidas en los datos recibidos, 
#         # ya que su ausencia indica que fueron eliminadas desde el frontend.
#         for image in existing_images:
#             # Verificar si la imagen actual está en la lista de imagenes_guardadas
#             if not any(img['image_name'] == image.image for img in imagenes_guardadas):
#                 # Construir la ruta completa a la imagen
#                 image_path = os.path.join(IMAGE_DIR, str(property_id), image.image)
#                 if os.path.exists(image_path):
#                     os.remove(image_path)  # Elimina el archivo de imagen del sistema de archivos
#                 db.delete(image)  # Elimina el registro de la imagen de la base de datos
#         db.commit()

#         # Guardar las nuevas imágenes en el sistema de archivos y en la base de datos
#         for base64_image in imagenes_nuevas:
#             image_data = base64.b64decode(base64_image['image_name'].split(",")[1])
#             id_aleatorio = str(uuid.uuid4()).replace('-', '1')[:8]
#             image_name = f"image_{id_aleatorio}{property_id}.jpg"
#             # Crear directorio específico para la propiedad si no existe
#             property_dir = os.path.join(IMAGE_DIR, str(property_id))
#             os.makedirs(property_dir, exist_ok=True)
#             file_path = os.path.join(property_dir, image_name)

#             # Guardar la imagen en el sistema de archivos
#             with open(file_path, "wb") as f:
#                 f.write(image_data)

#             # Guardar la nueva imagen en la base de datos
#             nueva_imagen = Imagen(property_id=property_id, image=image_name)
#             db.add(nueva_imagen)
#             db.commit()

#             imagenes_guardadas.append({
#                 "id_image": nueva_imagen.id,
#                 "image_name": nueva_imagen.image
#             })
#         # Retornar todas las imágenes (nuevas y existentes)
#         return {"status": "success", "imagenes": imagenes_guardadas}
       
#     except Exception as e:
#         db.rollback()
#         print(f"Error: {e}")
#         raise HTTPException(status_code=500, detail="Error al editar las imágenes de la propiedad")

#     finally:
#         db.close()
