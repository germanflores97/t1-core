from fastapi.testclient import TestClient
from copy import deepcopy

from src.app import app

__PREFIJO_URL_CLIENTES = "/clientes/"
__PREFIJO_URL_TARJETAS = "/tarjetas/"

tarjetas_test = TestClient(app)

request_crear_cliente = {
    "nombres": "Felix German", "apellido_paterno": "Flores", "apellido_materno": "Galvez",
    "curp": "FOGF970528HMSLLL04", "email": "germanflores97@outlook.com", "telefono": "527776015185"
}

request_crear_tarjeta = {
    "cliente_id": None, #Agregar manualmente el ID del cliente
    "numero_tarjeta": "5200828282828210",
    "cvv": "123",
    "expiracion": "12/25"
}

request_actualizar_tarjeta = {
    "cliente_id": None, #Agregar manualmente el ID del cliente
    "cvv": "456",
    "activa": False
}

def test_crud_tarjetas():
    request = deepcopy(request_crear_cliente)

    cliente_id = tarjetas_test.post(f"{__PREFIJO_URL_CLIENTES}", json=request).json()["respuesta"]["id"] #Se crea el cliente y se obtiene el ID

    request = deepcopy(request_crear_tarjeta)
    request["cliente_id"] = cliente_id
    response = tarjetas_test.post(f"{__PREFIJO_URL_TARJETAS}", json=request) #Se crea la tarjeta
    assert response.status_code in (200, 201) #201 cuando no existe y se crea, 200 en caso de existir
    tarjeta_id = response.json()["respuesta"]["id"]

    assert tarjetas_test.get(f"{__PREFIJO_URL_TARJETAS}{tarjeta_id}").status_code == 200 #Se consulta la tarjeta creada

    request = deepcopy(request_actualizar_tarjeta)
    request["cliente_id"] = cliente_id
    assert tarjetas_test.put(f"{__PREFIJO_URL_TARJETAS}{tarjeta_id}", json=request).status_code == 200 #Se actualiza la tarjeta

    assert tarjetas_test.delete(f"{__PREFIJO_URL_TARJETAS}{tarjeta_id}").status_code == 200 #Se elimina la tarjeta

    assert tarjetas_test.get(f"{__PREFIJO_URL_TARJETAS}{tarjeta_id}").status_code == 404 #Se consulta para validar que la tarjeta ya no existe

def test_tarjeta_no_cumple_lunh():
    request = deepcopy(request_crear_cliente)
    cliente_id = tarjetas_test.post(f"{__PREFIJO_URL_CLIENTES}", json=request).json()["respuesta"]["id"] #Se crea el cliente y se obtiene el ID

    request = deepcopy(request_crear_tarjeta)
    request["cliente_id"] = cliente_id
    request["numero_tarjeta"] = "5200828282828215" #No cumple con el algoritmo de Luhn

    response = tarjetas_test.post(f"{__PREFIJO_URL_TARJETAS}", json=request)
    assert response.status_code == 422