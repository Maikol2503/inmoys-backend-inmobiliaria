import json
from fastapi import APIRouter, HTTPException, Query, Path
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from config.db import Session

# Crear un enrutador de FastAPI
getContrato = APIRouter()

@getContrato.get("/contratos")
async def get_contratos(documento: str = Query(None, description="Documento del cliente para filtrar los contratos")):
    try:
        contratos_dict = {}

        with Session() as db:
            # Definir la consulta SQL base
            sql_query = text("""
                SELECT
                    contratos.id AS contrato_id,
                    clientes.nombre AS nombre_cliente,
                    clientes.apellido AS apellido_cliente,
                    clientes.documento AS documento_cliente,
                    properties.sku AS properties_sku,
                    properties.tipo AS properties_tipo,
                    properties.transaccion AS properties_transaccion,
                    properties.provincia AS properties_provincia,
                    properties.ciudad AS properties_ciudad,
                    properties.zona AS properties_zona,
                    properties.numeroCalle AS properties_numeroCalle,
                    properties.planta AS properties_planta,
                    properties.puerta AS properties_puerta,
                    contratos.fecha_creacion AS contrato_fecha_creacion
                FROM contratos
                INNER JOIN clientes ON clientes.id = contratos.client_id
                INNER JOIN properties ON properties.sku = contratos.property_sku
            """)

            # Si se proporciona un documento, agregar un filtro a la consulta
            if documento:
                sql_query = text("""
                    SELECT
                        contratos.id AS contrato_id,
                        clientes.nombre AS nombre_cliente,
                        clientes.apellido AS apellido_cliente,
                        clientes.documento AS documento_cliente,
                        properties.sku AS properties_sku,
                        properties.tipo AS properties_tipo,
                        properties.transaccion AS properties_transaccion,
                        properties.provincia AS properties_provincia,
                        properties.ciudad AS properties_ciudad,
                        properties.zona AS properties_zona,
                        properties.numeroCalle AS properties_numeroCalle,
                        properties.planta AS properties_planta,
                        properties.puerta AS properties_puerta,
                        contratos.fecha_creacion AS contrato_fecha_creacion
                    FROM contratos
                    INNER JOIN clientes ON clientes.id = contratos.client_id
                    INNER JOIN properties ON properties.sku = contratos.property_sku
                    WHERE clientes.documento = :documento
                """)
                result = db.execute(sql_query, {"documento": documento})
            else:
                result = db.execute(sql_query)
            
            rows = result.fetchall()

        # Construir la respuesta
        for row in rows:
            contrato_id = row.contrato_id
            if contrato_id not in contratos_dict:
                contratos_dict[contrato_id] = {
                    "id_contrato": contrato_id,
                    "sku": row.properties_sku,
                    "nombre_cliente": row.nombre_cliente,
                    "apellido_cliente": row.apellido_cliente,
                    "documento_cliente": row.documento_cliente,
                    "tipo_propiedad": row.properties_tipo,
                    "transaccion_propiedad": row.properties_transaccion,
                    "provincia_propiedad": row.properties_provincia,
                    "ciudad_propiedad": row.properties_ciudad,
                    "zona_propiedad": row.properties_zona,
                    "numeroCalle_propiedad": row.properties_numeroCalle,
                    "planta_propiedad": row.properties_planta,
                    "puerta_propiedad": row.properties_puerta,
                    "fecha_creacion_contrato": row.contrato_fecha_creacion
                }

        # Convertir el diccionario a una lista de contratos
        response = list(contratos_dict.values())
        return response

    except SQLAlchemyError as e:
        # Manejar errores de base de datos
        raise HTTPException(status_code=500, detail="Error en la base de datos")
    except Exception as e:
        # Manejar errores generales
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")























@getContrato.get("/contratos/{id}")
async def get_contrato_by_id(id: int = Path(..., description="ID del contrato a obtener")):
    print(f"Obteniendo contrato con ID: {id}")
    try:
        with Session() as db:
            sql_query = text("""
                SELECT
                    contratos.id AS contrato_id,
                    contratos.contrato_file AS contrato_file,
                    clientes.nombre AS nombre_cliente,
                    clientes.apellido AS apellido_cliente,
                    clientes.documento AS documento_cliente,
                    properties.id AS properties_id,
                    properties.sku AS properties_sku,
                    properties.tipo AS properties_tipo,
                    properties.transaccion AS properties_transaccion,
                    properties.provincia AS properties_provincia,
                    properties.ciudad AS properties_ciudad,
                    properties.zona AS properties_zona,
                    properties.numeroCalle AS properties_numeroCalle,
                    properties.planta AS properties_planta,
                    properties.puerta AS properties_puerta,
                    properties.precio AS properties_precio,
                    properties.disponibilidad AS properties_disponibilidad,
                    propietario.nombre AS propietario_nombre,
                    propietario.apellido AS propietario_apellido,
                    propietario.documento AS propietario_documento,
                    propietario.correo AS propietario_correo,
                    propietario.telefono AS propietario_telefono,
                    contratos.fecha_creacion AS contrato_fecha_creacion
                FROM contratos
                INNER JOIN clientes ON clientes.id = contratos.client_id
                INNER JOIN properties ON properties.sku = contratos.property_sku
                INNER JOIN propietario ON propietario.id = properties.propietario_id
                WHERE contratos.id = :id
            """)

            # Ejecutar la consulta
            result = db.execute(sql_query, {"id": id})
            row = result.fetchone()

            # Verificar si se encontró un contrato
            if not row:
                raise HTTPException(status_code=404, detail="Contrato no encontrado")

            # Construir el objeto de respuesta
            contrato = {
                "id_contrato": row.contrato_id,
                "contrato_file": row.contrato_file,
                "nombre_cliente": row.nombre_cliente,
                "apellido_cliente": row.apellido_cliente,
                "documento_cliente": row.documento_cliente,
                "property": {
                    "id": row.properties_id,
                    "sku": row.properties_sku,
                    "tipo": row.properties_tipo,
                    "transaccion": row.properties_transaccion,
                    "provincia": row.properties_provincia,
                    "ciudad": row.properties_ciudad,
                    "zona": row.properties_zona,
                    "numeroCalle": row.properties_numeroCalle,
                    "planta": row.properties_planta,
                    "puerta": row.properties_puerta,
                    "precio": row.properties_precio,
                    "disponibilidad": row.properties_disponibilidad
                },
                "propietario": {
                    "nombre": row.propietario_nombre,
                    "apellido": row.propietario_apellido,
                    "documento": row.propietario_documento,
                    "correo": row.propietario_correo,
                    "telefono": row.propietario_telefono
                },
                "fecha_creacion_contrato": row.contrato_fecha_creacion
            }

            print(f"Contrato encontrado: {contrato}")
            return contrato

    except SQLAlchemyError as e:
        print(f"Error en la base de datos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
