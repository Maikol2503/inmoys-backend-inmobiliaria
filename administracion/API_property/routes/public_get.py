import json
from fastapi import APIRouter, HTTPException
from config.db import Session
from sqlalchemy import text

# Crear un router para manejar las propiedades públicas
publicProperties = APIRouter()

# Consulta SQL sin datos sensibles
SQL_SELECT_PUBLIC_PROPERTIES = """
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
        imagesproperties.id AS image_id,
        imagesproperties.image AS image_name
    FROM properties
    INNER JOIN imagesproperties ON properties.id = imagesproperties.property_id
"""

# Función para construir la respuesta de propiedad pública
def build_public_property_dict(row):
    detalles_deserializados = json.loads(row.property_detalles)
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
        "image": [],
        "fecha_creacion": row.property_fecha_creacion
    }

# Función para obtener propiedades desde la base de datos
def fetch_public_properties(sql_query, params={}):
    with Session() as db:
        result = db.execute(text(sql_query), params)
        rows = result.fetchall()
    return rows












@publicProperties.get("/get-public-properties-disponibles")
async def get_public_properties(
    tipo: str = None,
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
    estadoInmueble: str = None
):
    try:
     
        query_conditions = ["properties.disponibilidad = 'disponible'"]

        if tipo:
            query_conditions.append(f"properties.tipo = '{tipo}'")
        if transaccion:
            query_conditions.append(f"properties.transaccion = '{transaccion}'")
        if ciudad:
            query_conditions.append(f"properties.ciudad = '{ciudad}'")
        if zona:
            query_conditions.append(f"(properties.zona LIKE '%{zona}%' OR properties.ciudad LIKE '%{zona}%')")
        if habitaciones:
            if numeroExactoHabitaciones == True:
                query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.habitaciones') = {habitaciones}")
            elif numeroExactoHabitaciones == False :
                query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.habitaciones') >= {habitaciones}")
        if banos:
            if numeroExactoBanos == True:
                query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.banos') = '{banos}'")
            elif numeroExactoBanos == False:
                query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.banos') >= '{banos}'")
        if garaje is not None and garaje == True:
            query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.garaje') = '{str(garaje).lower()}'")
        if piscina is not None and piscina == True:
            query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.piscina') = '{str(piscina).lower()}'")
        if trastero is not None and trastero == True:
            query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.trastero') = '{str(trastero).lower()}'")
        if jardin is not None and jardin == True:
            query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.jardin') = '{str(jardin).lower()}'")
        if ascensor is not None and ascensor  == True:
            query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.ascensor') = '{str(ascensor).lower()}'")
        if gimnasio is not None and gimnasio == True:
            query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.gimnasio') = '{str(gimnasio).lower()}'")
        if aireAcondicionado is not None and aireAcondicionado == True:
            query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.aire') = '{str(aireAcondicionado).lower()}'")
        if calefaccion is not None and calefaccion == True:
            query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.calefaccion') = '{str(calefaccion).lower()}'")
        if terraza is not None and terraza == True:
            query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.terraza') = '{str(terraza).lower()}'")
        if balcon is not None and balcon == True:
            query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.balcon') = '{str(balcon).lower()}'")
        
        
        # Filtro de precio en rango, solo si el valor es mayor que 0
        if precioDesde is not None and precioDesde > 0:
            query_conditions.append(f"properties.precio >= {precioDesde}")
        if precioHasta is not None and precioHasta > 0:
            query_conditions.append(f"properties.precio <= {precioHasta}")
        
        # Filtro de tamaño en rango, solo si el valor es mayor que 0
        if tamanoDesde is not None and tamanoDesde > 0:
            query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.tamano') >= {tamanoDesde}")
        if tamanoHasta is not None and tamanoHasta > 0:
            query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.tamano') <= {tamanoHasta}")
        if estadoInmueble is not None:
            query_conditions.append(f"JSON_UNQUOTE(properties.detalles->'$.estadoInmueble') = '{estadoInmueble}'")

        # Combinar todas las condiciones en la consulta
        where_clause = " AND ".join(query_conditions)
        
        sql_query = f"{SQL_SELECT_PUBLIC_PROPERTIES} WHERE {where_clause} ORDER BY properties.fecha_creacion DESC"
        print(sql_query)
        properties_dict = {}
        rows = fetch_public_properties(sql_query)
        
        for row in rows:
            property_id = row.property_id
            if property_id not in properties_dict:
                properties_dict[property_id] = build_public_property_dict(row)
                
            properties_dict[property_id]["image"].append({
                "id_image": row.image_id,
                "image_name": row.image_name
            })
        
        return list(properties_dict.values())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





















@publicProperties.get("/get-public-property-disponibles/{property_id}")
async def get_public_property_by_id(property_id: int):
    try:
        rows = fetch_public_properties(SQL_SELECT_PUBLIC_PROPERTIES + " WHERE properties.id = :property_id", {"property_id": property_id})
        
        if not rows:
            raise HTTPException(status_code=404, detail="Property not found")

        property_dict = build_public_property_dict(rows[0])
        
        for row in rows:
            property_dict["image"].append({
                "id_image": row.image_id,
                "image_name": row.image_name
            })
        
        return property_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




        # 


@publicProperties.get("/get-public-property-destacadas")
async def get_public_properties_destacadas():
    try:
        properties_dict = {}
        rows = fetch_public_properties(SQL_SELECT_PUBLIC_PROPERTIES + " WHERE properties.destacado = 1 AND properties.disponibilidad = 'disponible' ORDER BY properties.fecha_creacion DESC")
        
        for row in rows:
            property_id = row.property_id
            if property_id not in properties_dict:
                properties_dict[property_id] = build_public_property_dict(row)
                
            properties_dict[property_id]["image"].append({
                "id_image": row.image_id,
                "image_name": row.image_name
            })
        
        return list(properties_dict.values())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))