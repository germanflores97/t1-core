from bson import ObjectId
from src.cobros.models import Cobro
from src.core.mongo_db import get_db
from pymongo import DESCENDING

coleccion_cobros = get_db()["cobros"]

def crear_cobro(datos_cobro: Cobro):
    cobro_registrado = coleccion_cobros.insert_one(datos_cobro.to_mongo())

    return cobro_registrado.inserted_id

def consultar_cobros_por_tarjeta(tarjeta_id:str):
    return coleccion_cobros.find({"tarjeta_id": ObjectId(tarjeta_id)}).sort({"fecha_operacion": DESCENDING})