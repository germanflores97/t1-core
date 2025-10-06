from fastapi.testclient import TestClient

from src.app import app

__PREFIJO_URL_CLIENTES = "/clientes/"
__PREFIJO_URL_TARJETAS = "/tarjetas/"

tarjetas_test = TestClient(app)

def test_crud_tarjetas():
    request = {
        "nombres": "Felix German", "apellido_paterno": "Flores", "apellido_materno": "Galvez",
        "curp": "FOGF970528HMSLLL04", "email": "germanflores97@outlook.com", "telefono": "527776015185"
    }

    cliente_id = tarjetas_test.post(f"{__PREFIJO_URL_CLIENTES}", json=request).json()["respuesta"]["id"]

    request = {
        "cliente_id": cliente_id,
        "numero_tarjeta": "5200828282828210",
        "cvv": "123",
        "expiracion": "12/25"
    }
    response = tarjetas_test.post(f"{__PREFIJO_URL_TARJETAS}", json=request)
    assert response.status_code in (200, 201) #201 cuando no existe y se crea, 200 en caso de existir
    tarjeta_id = response.json()["respuesta"]["id"]

    assert tarjetas_test.get(f"{__PREFIJO_URL_TARJETAS}{tarjeta_id}").status_code == 200

    request = {
        "cliente_id": cliente_id,
        "cvv": "456",
        "activa": False
    }
    assert tarjetas_test.put(f"{__PREFIJO_URL_TARJETAS}{tarjeta_id}", json=request).status_code == 200

    assert tarjetas_test.delete(f"{__PREFIJO_URL_TARJETAS}{tarjeta_id}").status_code == 200

def test_tarjeta_no_cumple_lunh():
    request = {
        "nombres": "Felix German", "apellido_paterno": "Flores", "apellido_materno": "Galvez",
        "curp": "FOGF970528HMSLLL04", "email": "germanflores97@outlook.com", "telefono": "527776015185"
    }

    cliente_id = tarjetas_test.post(f"{__PREFIJO_URL_CLIENTES}", json=request).json()["respuesta"]["id"]

    request = {
        "cliente_id": cliente_id,
        "numero_tarjeta": "5200828282828215",
        "cvv": "123",
        "expiracion": "12/25"
    }
    response = tarjetas_test.post(f"{__PREFIJO_URL_TARJETAS}", json=request)
    assert response.status_code == 422