from src.cobros.models import Cobro
from src.core.mongo_db import get_db

coleccion_cobros = get_db()["cobros"]

def crear_cobro(datos_cobro: Cobro):
    cobro_registrado = coleccion_cobros.insert_one(datos_cobro.to_mongo())

    return cobro_registrado.inserted_id