from fastapi.testclient import TestClient
from datetime import datetime
from copy import deepcopy

from src.app import app
from src.core.settings import configs

__PREFIJO_URL_CLIENTES = "/clientes/"
__PREFIJO_URL_TARJETAS = "/tarjetas/"
__PREFIJO_URL_COBROS = "/cobros/"

__FORMATO_FECHA_OPERACION = "%Y/%m/%d %H:%M:%S"

cobros_test = TestClient(app)

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

request_aplicar_cobro = {
    "tarjeta_id": None, #Agregar manualmente el ID de la tarjeta
    "importe": 50.5,
    "fecha_operacion": datetime.now().strftime(__FORMATO_FECHA_OPERACION),
    "concepto": "test",
    "cvv": "123"
}

def test_cobros():
    request = deepcopy(request_crear_cliente)
    cliente_id = cobros_test.post(f"{__PREFIJO_URL_CLIENTES}", json=request).json()["respuesta"]["id"] #Se crea el cliente y se obtiene el ID

    request = deepcopy(request_crear_tarjeta)
    request["cliente_id"] = cliente_id
    response = cobros_test.post(f"{__PREFIJO_URL_TARJETAS}", json=request) #Se crea la tarjeta
    tarjeta_id = response.json()["respuesta"]["id"]

    request = deepcopy(request_aplicar_cobro)
    request["tarjeta_id"] = tarjeta_id
    response = cobros_test.post(f"{__PREFIJO_URL_COBROS}", json=request) #Aplicar cobro
    assert response.status_code == 200
    cobro_id = response.json()["respuesta"]["id"]

    response = cobros_test.get(f"{__PREFIJO_URL_COBROS}{cliente_id}") #Consulta cobros del cliente
    assert response.status_code == 200
    assert len(response.json()["respuesta"]["cobros"]) > 0 #Validar que existan cobros

    response = cobros_test.post(f"{__PREFIJO_URL_COBROS}{cobro_id}/reembolso") #Aplicar reembolso
    assert response.status_code == 200
    assert response.json()["respuesta"]["reembolsado"]

    assert not cobros_test.post(f"{__PREFIJO_URL_COBROS}{cobro_id}/reembolso").json()["respuesta"]["reembolsado"] #Validar que no se pueda reembolsar dos veces

def test_cobros_v2():
    request = deepcopy(request_crear_cliente)
    cliente_id = cobros_test.post(f"{__PREFIJO_URL_CLIENTES}", json=request).json()["respuesta"]["id"] #Se crea el cliente y se obtiene el ID

    request = deepcopy(request_crear_tarjeta)
    request["cliente_id"] = cliente_id
    response = cobros_test.post(f"{__PREFIJO_URL_TARJETAS}", json=request) #Se crea la tarjeta
    tarjeta_id = response.json()["respuesta"]["id"]

    request = deepcopy(request_aplicar_cobro)
    request["tarjeta_id"] = tarjeta_id
    response = cobros_test.post(f"{__PREFIJO_URL_COBROS}v2/", json=request) #Intenta aplicar cobro sin token
    assert response.status_code == 401 #No autorizado

    cobro_id_inventado = "68e42b60537b1edbc2030df1"
    response = cobros_test.post(f"{__PREFIJO_URL_COBROS}v2/{cobro_id_inventado}/reembolso") #Aplicar reembolso
    assert response.status_code == 401 #No autorizado

    request = {"username": configs().oauth2_user, "password": configs().oauth2_password}
    response = cobros_test.post(f"{__PREFIJO_URL_COBROS}auth/", data=request)
    assert response.status_code == 200

    header_authorization = {
        "Authorization": f"Bearer {response.json()["access_token"]}"
    }
    
    request = deepcopy(request_aplicar_cobro)
    request["tarjeta_id"] = tarjeta_id
    response = cobros_test.post(f"{__PREFIJO_URL_COBROS}v2/", json=request, headers=header_authorization) #Aplicar cobro con token
    assert response.status_code == 200 #Validar que el cobro se aplique
    cobro_id = response.json()["respuesta"]["id"]

    response = cobros_test.post(f"{__PREFIJO_URL_COBROS}v2/{cobro_id}/reembolso", headers=header_authorization) #Aplicar reembolso con token
    assert response.status_code == 200 #Validar que el reembolso se aplique
