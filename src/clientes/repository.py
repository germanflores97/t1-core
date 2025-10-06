from src.clientes.models import Cliente
from src.core.mongo_db import get_db
from bson import ObjectId
from typing import Dict

coleccion_clientes = get_db()["clientes"]

def crear_cliente(cliente: Cliente) -> str:
    cliente_registrado = coleccion_clientes.insert_one(cliente.to_mongo())

    return cliente_registrado.inserted_id

def actualizar_cliente(cliente: Cliente) -> int:
    registros_actualizados = coleccion_clientes.update_one(
        {"_id": cliente.id}, 
        {
            "$set": {
                "nombres": cliente.nombres,
                "apellido_paterno": cliente.apellido_paterno,
                "apellido_materno": cliente.apellido_materno,
                "curp": cliente.curp,
                "email": cliente.email,
                "telefono": cliente.telefono,
                "activo": cliente.activo,
                "fecha_actualizacion": cliente.fecha_actualizacion
            }
        }
    )
    
    return registros_actualizados.modified_count

def consultar_cliente(id: str) -> Dict | None:
    return coleccion_clientes.find_one({"_id": ObjectId(id)})

def consultar_cliente_por_curp(curp:str)  -> Dict | None:
    return coleccion_clientes.find_one({"curp": curp})

def eliminar_cliente(id: str) -> int:
    return coleccion_clientes.delete_one({"_id": ObjectId(id)}).deleted_count