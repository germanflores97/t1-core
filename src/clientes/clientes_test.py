from fastapi.testclient import TestClient
from copy import deepcopy

from src.app import app

__PREFIJO_URL_CLIENTES = "/clientes/"

cliente_test = TestClient(app)

request_crear_cliente = {
    "nombres": "Felix German", "apellido_paterno": "Flores", "apellido_materno": "Galvez",
    "curp": "FOGF970528HMSLLL04", "email": "germanflores97@outlook.com", "telefono": "527776015185"
}

request_actualizar_cliente = {
    "nombres": "Felix German", "apellido_paterno": "Flores", "apellido_materno": "Galvez", "curp": "FOGF970528HMSLLL04",
    "email": "germanflores97@outlook.com", "telefono": "527776015185", "activo": True
}

def test_crear_cliente_exitoso():
    request = deepcopy(request_crear_cliente)

    response = cliente_test.post(f"{__PREFIJO_URL_CLIENTES}", json=request)
    assert response.status_code in (200, 201) #201 cuando no existe y se crea, 200 en caso de existir

def test_crear_cliente_error_curp():
    request = deepcopy(request_crear_cliente)
    request["curp"] = "FOGF970528HMSLLL0" #Curp invalida

    response = cliente_test.post(f"{__PREFIJO_URL_CLIENTES}", json=request)
    assert response.status_code == 422

def test_crear_cliente_error_email():
    request = deepcopy(request_crear_cliente)
    request["email"] = "germanflores97@" #Email invalido

    response = cliente_test.post(f"{__PREFIJO_URL_CLIENTES}", json=request)
    assert response.status_code == 422

def test_consultar_cliente_exitoso():
    request = deepcopy(request_crear_cliente)
    cliente_id = cliente_test.post(f"{__PREFIJO_URL_CLIENTES}", json=request).json()["respuesta"]["id"]

    response = cliente_test.get(f"{__PREFIJO_URL_CLIENTES}{cliente_id}")
    assert response.status_code == 200

def test_consultar_cliente_inexistente():
    cliente_id = "68e42b60537b1edbc2030df1"
    
    response = cliente_test.get(f"{__PREFIJO_URL_CLIENTES}{cliente_id}")
    assert response.status_code == 404

def test_actualizar_cliente_exitoso():
    request = deepcopy(request_crear_cliente)
    cliente_id = cliente_test.post(f"{__PREFIJO_URL_CLIENTES}", json=request).json()["respuesta"]["id"] #Se crea el cliente y se obtiene el ID
    
    request = deepcopy(request_actualizar_cliente)
    nuevo_email = "pruebas@gmail.com"
    request["email"] = nuevo_email

    response = cliente_test.put(f"{__PREFIJO_URL_CLIENTES}{cliente_id}", json=request) #Se actualiza el correo del cliente
    assert response.status_code == 200

    response = cliente_test.get(f"{__PREFIJO_URL_CLIENTES}{cliente_id}") #Se consulta para validar que el correo se actualizo
    assert response.status_code == 200
    assert response.json()["respuesta"]["email"] == nuevo_email

def test_eliminar_cliente_exitoso():
    request = deepcopy(request_crear_cliente)
    cliente_id = cliente_test.post(f"{__PREFIJO_URL_CLIENTES}", json=request).json()["respuesta"]["id"] #Se crea el cliente y se obtiene el ID

    response = cliente_test.delete(f"{__PREFIJO_URL_CLIENTES}{cliente_id}") #Se elimina el cliente
    assert response.status_code == 200

    assert cliente_test.get(f"{__PREFIJO_URL_CLIENTES}{cliente_id}").status_code == 404 #Se consulta para validar que el cliente ya no existe