import json
from fastapi import APIRouter, HTTPException, Query
from config.db import Session
from sqlalchemy import text

# Crear un router para manejar las propiedades
getProperties = APIRouter()

# Consultas SQL
SQL_SELECT_PROPERTIES = """
    SELECT
        propietario.id AS propietario_id,
        propietario.nombre AS propietario_nombre,
        propietario.apellido AS propietario_apellido,
        propietario.documento AS propietario_documento,
        propietario.correo AS propietario_correo,
        propietario.telefono AS propietario_telefono,
        properties.sku AS property_sku,
        properties.id AS property_id,
        properties.destacado AS property_destacado,
        properties.descripcion AS property_descripcion,
        properties.precio AS property_precio,
        properties.tipo AS property_tipo,
        properties.transaccion AS property_transaccion,
        properties.disponibilidad AS property_disponibilidad,
        properties.provincia AS property_provincia,
        properties.ciudad AS property_ciudad,
        properties.zona AS property_zona,
        properties.puerta AS property_puerta,
        properties.numeroCalle AS property_numeroCalle,
        properties.nombreCalle AS property_nombreCalle,
        properties.cp AS property_cp,
        properties.planta AS property_planta,
        properties.detalles AS property_detalles,
        properties.propietario_id AS property_propietario_id,
        properties.fecha_creacion AS property_fecha_creacion,
        imagesproperties.id AS image_id,
        imagesproperties.image AS image_name
    FROM properties
    INNER JOIN imagesproperties ON properties.id = imagesproperties.property_id
    INNER JOIN propietario ON propietario.id = properties.propietario_id
"""

# Función para construir la respuesta de propiedad
def build_property_dict(row):
    detalles_deserializados = json.loads(row.property_detalles)
    return {
        "sku": row.property_sku,
        "id_property": row.property_id,
        "destacado": row.property_destacado,
        "nombre": row.propietario_nombre,
        "apellido": row.propietario_apellido,
        "documento": row.propietario_documento,
        "correo": row.propietario_correo,
        "telefono": row.propietario_telefono,
        "descripcion": row.property_descripcion,
        "precio": row.property_precio,
        "tipo": row.property_tipo,
        "transaccion": row.property_transaccion,
        "disponibilidad": row.property_disponibilidad,
        "provincia": row.property_provincia,
        "ciudad": row.property_ciudad,
        "zona": row.property_zona,
        "cp": row.property_cp,
        "puerta": row.property_puerta,
        "numeroCalle": row.property_numeroCalle,
        "nombreCalle": row.property_nombreCalle,
        "planta": row.property_planta,
        "detalles": detalles_deserializados,
        "propietario_id": row.property_propietario_id,
        "image": [],
        "fecha_creacion": row.property_fecha_creacion
    }

# Función para obtener propiedades desde la base de datos
def fetch_properties(sql_query, params={}):
    with Session() as db:
        result = db.execute(text(sql_query), params)
        rows = result.fetchall()
    return rows

# Rutas

@getProperties.get("/get-properties")
async def get_properties():
    try:
        properties_dict = {}
        rows = fetch_properties(SQL_SELECT_PROPERTIES + " ORDER BY properties.fecha_creacion DESC")
        
        for row in rows:
            property_id = row.property_id
            if property_id not in properties_dict:
                properties_dict[property_id] = build_property_dict(row)
                
            properties_dict[property_id]["image"].append({
                "id_image": row.image_id,
                "image_name": row.image_name
            })
        
        return list(properties_dict.values())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    





@getProperties.get("/get-properties-disponibles")
async def get_properties_disponibles():
    try:
        properties_dict = {}
        rows = fetch_properties(SQL_SELECT_PROPERTIES + " WHERE properties.disponibilidad = 'disponible' ORDER BY properties.fecha_creacion DESC")
        
        for row in rows:
            property_id = row.property_id
            if property_id not in properties_dict:
                properties_dict[property_id] = build_property_dict(row)
                
            properties_dict[property_id]["image"].append({
                "id_image": row.image_id,
                "image_name": row.image_name
            })
        
        return list(properties_dict.values())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





@getProperties.get("/get-property/{property_id}")
async def get_property_by_id(property_id: int):
    try:
        rows = fetch_properties(SQL_SELECT_PROPERTIES + " WHERE properties.id = :property_id", {"property_id": property_id})
        
        if not rows:
            raise HTTPException(status_code=404, detail="Property not found")

        property_dict = build_property_dict(rows[0])
        
        for row in rows:
            property_dict["image"].append({
                "id_image": row.image_id,
                "image_name": row.image_name
            })
        
        return property_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    













@getProperties.get("/get-property-by-sku-similar/{sku}")
async def get_property_by_sku_similar(sku: str):
    try:
        # Consulta SQL segura que usa LIKE para buscar SKU similares
        query = SQL_SELECT_PROPERTIES + """
            WHERE properties.sku LIKE :sku
        """
        
        # Ejecutar la consulta usando parámetros
        rows = fetch_properties(query, {"sku": f"%{sku}%"})
        
        if not rows:
            raise HTTPException(status_code=404, detail="No se encontraron propiedades similares al SKU")

        # Construir la respuesta de propiedad
        properties_dict = {}
        for row in rows:
            property_id = row.property_id
            if property_id not in properties_dict:
                properties_dict[property_id] = build_property_dict(row)
            
            # Agregar las imágenes a la propiedad
            properties_dict[property_id]["image"].append({
                "id_image": row.image_id,
                "image_name": row.image_name
            })

        return list(properties_dict.values())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))















@getProperties.get("/get-properties-tipo")
async def get_properties_por_tipo_transaccion(tipoTransaccion: str = Query(None, description="Tipo de transacción: alquiler o venta")):
    try:
        properties_dict = {}
        query = SQL_SELECT_PROPERTIES + " WHERE properties.transaccion = :tipoTransaccion  AND properties.disponibilidad = 'disponible'"
        rows = fetch_properties(query, {"tipoTransaccion": tipoTransaccion})
        
        for row in rows:
            property_id = row.property_id
            if property_id not in properties_dict:
                properties_dict[property_id] = build_property_dict(row)
                
            properties_dict[property_id]["image"].append({
                "id_image": row.image_id,
                "image_name": row.image_name
            })

        return list(properties_dict.values())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@getProperties.get("/validar-sku/{sku}")
async def validar_sku(sku: str):
    try:
        query = "SELECT COUNT(*) AS sku_count FROM properties WHERE sku = :sku"
        rows = fetch_properties(query, {"sku": sku})
        
        if rows[0].sku_count > 0:
            return {"exists": True}
        else:
            raise HTTPException(status_code=404, detail="SKU no encontrado")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
