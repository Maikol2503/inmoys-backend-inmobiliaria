# from fastapi import APIRouter, HTTPException
# import httpx
# from pydantic_core import Url
# from sqlalchemy.exc import SQLAlchemyError
# from administracion.API_clients.schemas.clientSchema import ClientSchema
# from administracion.API_contrato.models.contartoModel import ContratoModel
# from administracion.API_contrato.schema.contratoSchema import ContratoSchema
# from config.db import Session

# # Crear una sesión de base de datos
# db = Session()
# addContrato = APIRouter()
# url = 'http://localhost:8000/'

# @addContrato.post("/agregar-contrato")
# async def create_contrato(contrato: ContratoSchema):
#     try:
#          # Validar si el SKU existe
#         if not await validar_sku(contrato.property_sku):
#             raise HTTPException(status_code=404, detail="SKU no encontrado")

#         # Preparar datos del cliente
#         dataClient = {
#             "id":0,
#             "nombre": contrato.nombre,
#             "apellido": contrato.apellido,
#             "documento": contrato.documento,
#             "telefono": contrato.telefono,
#             "correo": contrato.correo,
#         }
#         print('dataclient ',dataClient)

#         # Agregar cliente
#         dataNewClient = await addClient(dataClient)
#         print(f"Cliente creado: {dataNewClient}")

#         # Preparar datos del nuevo contrato
#         dataNewContrato = {
#             'property_sku': contrato.property_sku,
#             'client_id': dataNewClient['id'],
#             'contrato_file': contrato.contrato_file
#         }
#         print(f"Datos del nuevo contrato: {dataNewContrato}")

#         # Crear una nueva instancia del contrato usando los datos proporcionados
#         new_contrato = ContratoModel(**dataNewContrato)
#         print(f"Instancia de contrato creada: {new_contrato}")

#         # Añadir el nuevo contrato a la base de datos y hacer commit
#         db.add(new_contrato)
#         db.commit()

#         # Refrescar la instancia del contrato con los datos actualizados
#         db.refresh(new_contrato)
#         print(f"Contrato guardado: {new_contrato}")
        
#         return new_contrato

#     except HTTPException as e:
#         # Relevanta el error HTTP tal cual
#         raise e
#     except SQLAlchemyError as e:
#         # Captura errores relacionados con la base de datos
#         db.rollback()  # Revertir los cambios en caso de error
#         raise HTTPException(status_code=500, detail="Error en la base de datos")
#     except Exception as e:
#         # Captura cualquier otro error inesperado
#         raise HTTPException(status_code=500, detail="Error inesperado")








# async def addClient(dataClient:ClientSchema):
#     async with httpx.AsyncClient() as client:
#         response = await client.post(f"{url}agregar-cliente", json=dataClient)
#         # Verificar que la respuesta sea exitosa
#         if response.status_code == 200:
#             response_json = response.json()
#             # print(response_json)
#             return response_json['dataNewClient']
            
           
#         else:
#             # Manejar el caso de error HTTP
#             raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error desconocido"))




# async def validar_sku(sku: str) -> bool:
#     async with httpx.AsyncClient() as client:
#         response = await client.get(f"{url}validar-sku/{sku}")
#         # Verificar que la respuesta sea exitosa y que el SKU exista
#         if response.status_code == 200:
#             response_json = response.json()
#             return response_json.get('exists')
#         else:
#             return False