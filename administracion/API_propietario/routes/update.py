# from fastapi import APIRouter, HTTPException
# from administracion.API_propietario.models import PropietarioModel
# from administracion.API_propietario.schemas import DatosPropietario
# from config.db import Session

# # Crear un enrutador para gestionar los propietarios
# updatePropietario = APIRouter()

# @updatePropietario.put("/editar-propietario/{propietario_id}")
# async def edit_propietario(propietario_id: int, updated_propietario: DatosPropietario):
#     # Instanciar la sesión de base de datos
#     db = Session()
    
#     try:
#         # Obtener el propietario existente de la base de datos
#         existing_client = db.query(PropietarioModel).filter(PropietarioModel.id == propietario_id).first()

#         # Si el propietario no existe, lanzar un error 404
#         if not existing_client:
#             raise HTTPException(status_code=404, detail="Propietario no encontrado")

#         # Actualizar la información del propietario con los nuevos datos
#         for key, value in updated_propietario.dict().items():
#             setattr(existing_client, key, value)

#         # Confirmar los cambios en la base de datos
#         db.commit()
#         # Refrescar el objeto existente para reflejar los cambios realizados
#         db.refresh(existing_client)

#         # Retornar el propietario actualizado
#         return existing_client

#     except Exception as e:
#         # En caso de error, deshacer los cambios
#         db.rollback()
#         raise HTTPException(status_code=500, detail=f"Error al editar el propietario: {str(e)}")

#     finally:
#         # Cerrar la sesión de base de datos
#         db.close()
