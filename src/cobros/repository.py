from bson import ObjectId
from src.cobros.models import Cobro
from src.core.mongo_db import get_db
from pymongo import DESCENDING
from typing import Dict
from datetime import datetime

coleccion_cobros = get_db()["cobros"]

def crear_cobro(datos_cobro: Cobro) -> str:
    cobro_registrado = coleccion_cobros.insert_one(datos_cobro.to_mongo())

    return str(cobro_registrado.inserted_id)

def consultar_cobro(id: str) -> Dict | None:
    return coleccion_cobros.find_one({"_id": ObjectId(id)})

def consultar_cobros_por_tarjeta(tarjeta_id:str):
    return coleccion_cobros.find({"tarjeta_id": ObjectId(tarjeta_id)}).sort({"fecha_operacion": DESCENDING})

def aplicar_reembolso(id:str) -> int:
    fecha_reembolso = datetime.now()

    registros_actualizados = coleccion_cobros.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "reembolsado": True,
                "fecha_actualizacion": fecha_reembolso,
                "fecha_reembolso": fecha_reembolso
            }
        }
    )

    return registros_actualizados.modified_count