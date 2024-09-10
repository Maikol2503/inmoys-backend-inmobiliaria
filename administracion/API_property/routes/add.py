from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import httpx
from administracion.API_property.createData import CreateData
from administracion.API_property.images_propertys.schemas.image_request import ImageRequest
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

@addProperties.post("/api/publicar-propiedad/")
async def create_property(property:DatosPropiedad):
   

    datos_propietario = {
        'nombre':property.nombre,
        'apellido':property.apellido,
        'documento':property.documento,
        'correo':property.correo,
        'telefono':property.telefono
        }
     
    if(property.tipo == 'vivienda'):
        datos_propiedad = CreateData().vivienda(property)
    elif (property.tipo == 'oficina'):
        datos_propiedad = CreateData().oficina(property)
    elif (property.tipo == 'terreno'):
        datos_propiedad = CreateData().terreno(property)

    imagenes = property.image
 
    try:
        id_propietario = await addPropietario(datos_propietario)
        id_new_property = await addProperty(id_propietario, datos_propiedad )
        imagenes_list = await addImagenProperty(id_new_property, imagenes)
        datos_combinados = {**datos_propietario, **datos_propiedad}
        datos_combinados["id_property"] = id_new_property
        datos_combinados["image"] = imagenes_list
      
        return datos_combinados
    except HTTPException as e:      
        raise e
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al crear la propiedad")
    finally:
        db.close()





async def addPropietario(data: dict) -> int:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{url}agregar-propietario", json=data)
        if response.status_code == 200:
            cliente_data = response.json()
            cliente_id = cliente_data.get("id")
            if cliente_id is not None:
                return cliente_id
            else:
                raise HTTPException(status_code=500, detail="No se recibió el ID del cliente.")
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error desconocido"))



async def addProperty(id_propietario: int, data: PropertySchema):
    try:
        # Crear una nueva propiedad usando el id_client y los datos de la propiedad
        new_property = Property(propietario_id=id_propietario, **data)
        db.add(new_property)
        db.commit()
        db.refresh(new_property)
        return new_property.id
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al crear la propiedad")


async def addImagenProperty(id_property:int, imagenes:ImageRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{url}agregar-imagenes-propiedad", json={'id_property':id_property, 'image':imagenes})
        # Verificar que la respuesta sea exitosa
        if response.status_code == 200:
            response_json = response.json()
            return response_json['imagenes']
            
           
        else:
            # Manejar el caso de error HTTP
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error desconocido"))


