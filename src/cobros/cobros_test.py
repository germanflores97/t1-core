from fastapi.testclient import TestClient
from datetime import datetime

from src.app import app

__PREFIJO_URL_CLIENTES = "/clientes/"
__PREFIJO_URL_TARJETAS = "/tarjetas/"
__PREFIJO_URL_COBROS = "/cobros/"

__FORMATO_FECHA_OPERACION = "%Y/%m/%d %H:%M:%S"

cobros_test = TestClient(app)

def test_cobros():
    request = {
        "nombres": "Felix German", "apellido_paterno": "Flores", "apellido_materno": "Galvez",
        "curp": "FOGF970528HMSLLL04", "email": "germanflores97@outlook.com", "telefono": "527776015185"
    }

    cliente_id = cobros_test.post(f"{__PREFIJO_URL_CLIENTES}", json=request).json()["respuesta"]["id"]

    request = {
        "cliente_id": cliente_id,
        "numero_tarjeta": "5200828282828210",
        "cvv": "123",
        "expiracion": "12/25"
    }
    response = cobros_test.post(f"{__PREFIJO_URL_TARJETAS}", json=request)

    tarjeta_id = response.json()["respuesta"]["id"]
    request = {
        "tarjeta_id": tarjeta_id,
        "importe": 50.5,
        "fecha_operacion": datetime.now().strftime(__FORMATO_FECHA_OPERACION),
        "concepto": "test",
        "cvv": "123"
    }
    
    response = cobros_test.post(f"{__PREFIJO_URL_COBROS}", json=request) #Aplicar cobro
    assert response.status_code == 200
    cobro_id = response.json()["respuesta"]["id"]

    response = cobros_test.get(f"{__PREFIJO_URL_COBROS}{cliente_id}") #Consulta amigos
    assert response.status_code == 200
    assert len(response.json()["respuesta"]["cobros"]) > 0

    response = cobros_test.post(f"{__PREFIJO_URL_COBROS}{cobro_id}/reembolso") #Aplicar reembolso
    assert response.status_code == 200
    assert response.json()["respuesta"]["reembolsado"]



