from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from administracion.API_clients.models.clientsModel import ClientModel
from administracion.API_clients.schemas.clientSchema import ClientSchema
from config.db import Session

addClient = APIRouter()

@addClient.post("/agregar-cliente")
async def create_client(cliente: ClientSchema):
    db = Session()  # Abrir sesión de base de datos aquí
    try:
        # Imprimir el cuerpo de la solicitud recibido para depuración
        print("Cuerpo de la solicitud recibido:", cliente.dict())

        # Crear una nueva instancia del cliente usando los datos proporcionados
        new_client = ClientModel(
            nombre=cliente.nombre,
            apellido=cliente.apellido,
            documento=cliente.documento,
            telefono=cliente.telefono,
            correo=cliente.correo
        )
        
        # Añadir el nuevo cliente a la base de datos y hacer commit
        db.add(new_client)
        db.commit()
        
        # Refrescar la instancia del cliente con los datos actualizados
        db.refresh(new_client)

        # Preparar los datos del cliente para la respuesta
        client_data = {
            "id": new_client.id,
            "nombre": new_client.nombre,
            "apellido": new_client.apellido,
            "documento": new_client.documento,
            "telefono": new_client.telefono,
            "correo": new_client.correo
        }

        print("Cliente agregado:", client_data)
        return {'message': 'Cliente agregado correctamente', 'dataNewClient': client_data}

    except SQLAlchemyError as e:
        # Captura errores relacionados con la base de datos
        db.rollback()  # Revertir los cambios en caso de error
        raise HTTPException(status_code=500, detail="Error en la base de datos")
    
    except Exception as e:
        # Captura cualquier otro error inesperado
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

    finally:
        db.close()  # Cerrar la sesión aquí
