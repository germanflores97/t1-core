from bson import ObjectId
from typing import Dict
from src.core.mongo_db import get_db
from src.tarjetas.models import Tarjeta

coleccion_tarjetas = get_db()["tarjetas"]

def crear_tarjeta(datos_tarjeta: Tarjeta) -> str:
    tarjeta_registrada = coleccion_tarjetas.insert_one(datos_tarjeta.to_mongo())

    return tarjeta_registrada.inserted_id

def consultar_tarjeta(id:str) -> Dict | None:
    return coleccion_tarjetas.find_one({"_id": ObjectId(id)})

def consultar_tarjeta_por_cliente_id_bin_terminacion(cliente_id:str, bin:str, terminacion:str):
    return coleccion_tarjetas.find_one({"cliente_id": ObjectId(cliente_id), "bin": bin, "terminacion": terminacion})

def actualizar_tarjeta(tarjeta: Tarjeta) -> int:
    registros_actualizados = coleccion_tarjetas.update_one(
        {"_id": tarjeta.id},
        {
            "$set": {
                "cliente_id": tarjeta.cliente_id,
                "cvv": tarjeta.cvv,
                "activa": tarjeta.activa,
                "fecha_actualizacion": tarjeta.fecha_actualizacion
            }
        }
    )

    return registros_actualizados.modified_count

def eliminar_tarjeta(id:str) -> int:
    return coleccion_tarjetas.delete_one({"_id": ObjectId(id)}).deleted_count