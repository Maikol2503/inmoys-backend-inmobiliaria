from ast import Num
import json
import re
from typing import List
from fastapi import APIRouter, HTTPException, Query
from matplotlib.pyplot import ginput
from sympy import limit
from config.db import Session
from sqlalchemy import text

# Crear un router para manejar las propiedades
getProperties = APIRouter()

# Consultas SQL
SQL_SELECT_PROPERTIES = """
    SELECT
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
        properties.fecha_creacion AS property_fecha_creacion,
        properties.image AS property_image
    FROM properties
"""

# Función para construir la respuesta de propiedad
def build_property_dict(row):
    detalles_deserializados = json.loads(row.property_detalles)
    imagenes_deserializados = json.loads(row.property_image)
    return {
        "sku": row.property_sku,
        "id_property": row.property_id,
        "destacado": row.property_destacado,
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
        "image": imagenes_deserializados,
        "fecha_creacion": row.property_fecha_creacion
    }


def applyPagination(page:int, limit:int):
    offset = (page - 1) * limit  # Calcula el OFFSET correctamente
    text = f"""
    LIMIT {limit} OFFSET {offset}"""
    return text


# Función para obtener propiedades desde la base de datos
def fetch_properties(sql_query, params={}):
    with Session() as db:
        result = db.execute(text(sql_query), params)
        rows = result.fetchall()
        
    return rows


#Todas las propiedades tanto disponibles como no disponibles
@getProperties.get("/get-properties-filter")
async def get_properties(tipo: str = None,
    transaccion: str = None,
    ciudad: str = None,
    zona: str = None,
    habitaciones: int = None,
    banos: int = None,
    precioDesde: int = None,
    precioHasta: int = None,
    tamanoDesde: int = None,
    tamanoHasta: int = None,
    numeroExactoHabitaciones: bool = None,
    numeroExactoBanos: bool = None,
    garaje: bool = None,
    piscina: bool = None,
    trastero: bool = None,
    jardin: bool = None,
    ascensor: bool = None,
    gimnasio: bool = None,
    aireAcondicionado: bool = None,
    calefaccion: bool = None,
    terraza: bool = None,
    balcon: bool = None,
    estadoInmueble: str = None,
    order: str = "recientes",
    limit: int = 20,
    offset: int = 1):
    try:
        # Lista de filtros dinámicos
        query_conditions = ["properties.disponibilidad = 'disponible'"]
        params = {}
        # Filtros condicionales
        if tipo:
            query_conditions.append("properties.tipo = :tipo")
            params["tipo"] = tipo
        if transaccion:
            query_conditions.append("properties.transaccion = :transaccion")
            params["transaccion"] = transaccion
        if ciudad:
            query_conditions.append("properties.ciudad = :ciudad")
            params["ciudad"] = ciudad
        if zona:
            query_conditions.append("(properties.zona LIKE :zona OR properties.ciudad LIKE :zona)")
            params["zona"] = f"%{zona}%"
        if habitaciones:
            if numeroExactoHabitaciones == True:
                query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.habitaciones') = :habitaciones")
                params["habitaciones"] = habitaciones
            elif numeroExactoHabitaciones == False :
                query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.habitaciones') >= :habitaciones")
                params["habitaciones"] = habitaciones
        if banos:
            if numeroExactoBanos == True:
                query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.banos') = :banos")
                params["banos"] = banos
            elif numeroExactoBanos == False :
                query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.banos') >= :banos")
                params["banos"] = banos
        if garaje is not None and garaje == True:
            query_conditions.append("JSON_UNQUOTE(properties.detalles->'$.garaje') = :garaje")
            params["garaje"] = str(garaje).lower()
        if piscina is not None and piscina == True:
            query_conditions.append("JSON_UNQUOTE(properties.detalles->'$.piscina') = :piscina")
            params["piscina"] = str(piscina).lower()
        if gimnasio is not None and gimnasio == True:
            query_conditions.append("JSON_UNQUOTE(properties.detalles->'$.gimnasio') = :gimnasio")
            params["gimnasio"] = str(gimnasio).lower()
        if aireAcondicionado is not None and aireAcondicionado == True:
            query_conditions.append("JSON_UNQUOTE(properties.detalles->'$.aireAcondicionado') = :aireAcondicionado")
            params["aireAcondicionado"] = str(aireAcondicionado).lower()
        if trastero is not None and trastero == True:
            query_conditions.append("JSON_UNQUOTE(properties.detalles->'$.trastero') = :trastero")
            params["trastero"] = str(trastero).lower()
        if jardin is not None and jardin == True:
            query_conditions.append("JSON_UNQUOTE(properties.detalles->'$.jardin') = :jardin")
            params["jardin"] = str(jardin).lower()
        if ascensor is not None and ascensor == True:
            query_conditions.append("JSON_UNQUOTE(properties.detalles->'$.ascensor') = :ascensor")
            params["ascensor"] = str(ascensor).lower()
        if calefaccion is not None and calefaccion == True:
            query_conditions.append("JSON_UNQUOTE(properties.detalles->'$.calefaccion') = :calefaccion")
            params["calefaccion"] = str(calefaccion).lower()
        if terraza is not None and terraza == True:
            query_conditions.append("JSON_UNQUOTE(properties.detalles->'$.terraza') = :terraza")
            params["terraza"] = str(terraza).lower()
        if balcon is not None and balcon == True:
            query_conditions.append("JSON_UNQUOTE(properties.detalles->'$.balcon') = :balcon")
            params["balcon"] = str(balcon).lower()
        if precioDesde is not None and precioDesde > 0:
            query_conditions.append("properties.precio >= :precioDesde")
            params["precioDesde"] = precioDesde
        if precioHasta is not None and precioHasta > 0:
            query_conditions.append("properties.precio <= :precioHasta")
            params["precioHasta"] = precioHasta
        if tamanoDesde is not None and tamanoDesde > 0:
            query_conditions.append("JSON_UNQUOTE(properties.detalles->'$.tamano') >= :tamanoDesde")
            params["tamanoDesde"] = tamanoDesde
        if tamanoHasta is not None and tamanoHasta > 0:
            query_conditions.append("JSON_UNQUOTE(properties.detalles->'$.tamano') <= :tamanoHasta")
            params["tamanoHasta"] = tamanoHasta
        if estadoInmueble:
            query_conditions.append("JSON_UNQUOTE(properties.detalles->'$.estadoInmueble') = :estadoInmueble")
            params["estadoInmueble"] = estadoInmueble
        # Construir la consulta
        where_clause = " AND ".join(query_conditions)
        # Cláusula ORDER BY
        order_by_clause = {
            "relevancia": "ORDER BY properties.destacado DESC, properties.fecha_creacion DESC",
            "MasBaratos": "ORDER BY properties.precio ASC",
            "MasCaros": "ORDER BY properties.precio DESC",
        }.get(order, "ORDER BY properties.fecha_creacion DESC")
        # Consulta final con paginación
        sql_query = f"""
            {SQL_SELECT_PROPERTIES}
            WHERE {where_clause}
            {order_by_clause}
            
            LIMIT :limit OFFSET :offset
        """
        params["limit"] = limit
        params["offset"] = (offset - 1) * limit
        # Ejecutar consulta
        rows = fetch_properties(sql_query, params)
        # Construir resultado
        properties_dict = {}
        
        for row in rows:
            property_id = row.property_id
            if property_id not in properties_dict:
                properties_dict[property_id] = build_property_dict(row)
        return list(properties_dict.values())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


#todas las porpiedades disponibles
@getProperties.get("/get-properties-disponibles")
async def get_properties_disponibles(page:int=Query(), limit:int=Query()):
    try:
        paginacion = applyPagination(page, limit)
        rows = fetch_properties(SQL_SELECT_PROPERTIES + " WHERE properties.disponibilidad = 'disponible' ORDER BY properties.fecha_creacion DESC"+paginacion)
        properties_dict = {}
        for row in rows:
            property_id = row.property_id
            if property_id not in properties_dict:
                properties_dict[property_id] = build_property_dict(row)
        return list(properties_dict.values())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#se obtiene uan propiedad por el id
@getProperties.get("/get-property/{property_id}")
async def get_property_by_id(property_id: int):
    try:
        rows = fetch_properties(SQL_SELECT_PROPERTIES + " WHERE properties.id = :property_id", {"property_id": property_id})
        if not rows:
            raise HTTPException(status_code=404, detail="Property not found")
        property_dict = build_property_dict(rows[0])
        return property_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

#se obtiene uan propiedad por el sku
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
        property_dict = build_property_dict(rows[0])
        return property_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# se obtiene el total de propiedades siponibles, el total en alquiler y el total en ventas
@getProperties.get("/properties-count")
def properties_count():
    query = """SELECT 
    COUNT(CASE WHEN properties.transaccion = 'alquiler' AND properties.disponibilidad = 'disponible' THEN 1 END) AS total_properties_alquiler_disponibles,
    COUNT(CASE WHEN properties.transaccion = 'venta' AND properties.disponibilidad = 'disponible' THEN 1 END) AS total_properties_venta_disponibles,
    COUNT(CASE WHEN properties.disponibilidad = 'disponible' THEN 1 END) AS total_properties_disponibles,
    COUNT(*) AS total_properties
    FROM properties;"""
    data = {}
    with Session() as db:
        result = db.execute(text(query))
        rows = result.fetchall()
        for i, key in enumerate(result.keys()):
            data[key] = rows[0][i]
    return data


#validar si existe el sku
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







