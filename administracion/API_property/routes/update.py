from fastapi import APIRouter, HTTPException, Depends
import httpx
from administracion.API_property.createData import CreateData
from administracion.API_property.images_propertys.schemas.image_request import ImageRequest
from administracion.API_property.models.propertys_model import Property
from administracion.API_property.schemas.data_property_create import DatosPropiedad
from administracion.API_property.schemas.property import PropertySchema
from config.db import Session
from faker import Faker


fake = Faker()
updateProperties = APIRouter()
db = Session()
url = 'http://localhost:8000/'


@updateProperties.put('/editar-propiedad/{property_id}')
async def updatePropertie(property_id:int, property:DatosPropiedad):
    

    # Get the existing property
    existing_property = db.query(Property).filter(Property.id == property_id).first()
    
    if not existing_property:
        raise HTTPException(status_code=404, detail="Property not found")
    datos_propietario = {
        'nombre': property.nombre,
        'apellido': property.apellido,
        'documento': property.documento,
        'correo': property.correo,
        'telefono': property.telefono
    }

     
    if(property.tipo == 'vivienda'):
        datos_propiedad = CreateData().vivienda(property)
    elif (property.tipo == 'oficina'):
        datos_propiedad = CreateData().oficina(property)
    elif (property.tipo == 'terreno'):
        datos_propiedad = CreateData().terreno(property)

    imagenes = {'image':property.image}
   
    try:
        propietario_data_editada = await updatePropietario(existing_property.propietario_id, datos_propietario)
        propiedad_data_editada = await updateProperty(existing_property, datos_propiedad)
        imagenes_editadas = await addImagenProperty(property_id, imagenes)

        datos_combinados = {**propietario_data_editada, **propiedad_data_editada}

        print(datos_combinados)
        datos_combinados["id_property"] = property_id
        datos_combinados["image"] = imagenes_editadas

        return datos_combinados


    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al editar la propiedad")
    finally:
         db.close()


async def updatePropietario(propietario_id: int, data: dict) -> int:
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{url}editar-propietario/{propietario_id}", json=data)
        if response.status_code == 200:
            propietario_data = response.json()
            return propietario_data
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error desconocido"))


async def updateProperty(existing_property: Property, data: PropertySchema):
    try:
        for key, value in data.items():
            setattr(existing_property, key, value)
        
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


async def addImagenProperty(id_property:int, imagenes:ImageRequest):
    
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{url}editar-imagenes-propiedad/{id_property}", json=imagenes)
        # Verificar que la respuesta sea exitosa
        if response.status_code == 200:
            response_json = response.json()
            return response_json['imagenes']
            
            
        else:
            # Manejar el caso de error HTTP
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error desconocido"))