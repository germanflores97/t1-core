from fastapi.testclient import TestClient

from src.app import app

__PREFIJO_URL_CLIENTES = "/clientes/"

cliente_test = TestClient(app)

def test_crear_cliente_exitoso():
    request = {
        "nombres": "Felix German", "apellido_paterno": "Flores", "apellido_materno": "Galvez",
        "curp": "FOGF970528HMSLLL04", "email": "germanflores97@outlook.com", "telefono": "527776015185"
    }

    response = cliente_test.post(f"{__PREFIJO_URL_CLIENTES}", json=request)
    assert response.status_code in (200, 201) #201 cuando no existe y se crea, 200 en caso de existir

def test_crear_cliente_error_curp():
    request = {
        "nombres": "Felix German", "apellido_paterno": "Flores", "apellido_materno": "Galvez",
        "curp": "FOGF970528HMSLLL", "email": "germanflores97@outlook.com", "telefono": "527776015185"
    }

    response = cliente_test.post(f"{__PREFIJO_URL_CLIENTES}", json=request)
    assert response.status_code == 422

def test_crear_cliente_error_email():
    request = {
        "nombres": "Felix German", "apellido_paterno": "Flores", "apellido_materno": "Galvez",
        "curp": "FOGF970528HMSLLL04", "email": "germanflore", "telefono": "527776015185"
    }

    response = cliente_test.post(f"{__PREFIJO_URL_CLIENTES}", json=request)
    assert response.status_code == 422

def test_consultar_cliente_exitoso():
    request = {
        "nombres": "Felix German", "apellido_paterno": "Flores", "apellido_materno": "Galvez",
        "curp": "FOGF970528HMSLLL04", "email": "germanflores97@outlook.com", "telefono": "527776015185"
    }
    cliente_id = cliente_test.post(f"{__PREFIJO_URL_CLIENTES}", json=request).json()["respuesta"]["id"]

    response = cliente_test.get(f"{__PREFIJO_URL_CLIENTES}{cliente_id}")
    assert response.status_code == 200

def test_consultar_cliente_inexistente():
    cliente_id = "68e42b60537b1edbc2030df1"
    
    response = cliente_test.get(f"{__PREFIJO_URL_CLIENTES}{cliente_id}")
    assert response.status_code == 404

def test_actualizar_cliente_exitoso():
    request = {
        "nombres": "Felix German", "apellido_paterno": "Flores", "apellido_materno": "Galvez",
        "curp": "FOGF970528HMSLLL04", "email": "germanflores97@outlook.com", "telefono": "527776015185",
        "activo": True
    }
    cliente_id = cliente_test.post(f"{__PREFIJO_URL_CLIENTES}", json=request).json()["respuesta"]["id"]
    
    nuevo_email = "pruebas@gmail.com"
    request["email"] = nuevo_email

    response = cliente_test.put(f"{__PREFIJO_URL_CLIENTES}{cliente_id}", json=request)
    assert response.status_code == 200

    response = cliente_test.get(f"{__PREFIJO_URL_CLIENTES}{cliente_id}")
    assert response.json()["respuesta"]["email"] == nuevo_email

def test_eliminar_cliente_exitoso():
    request = {
        "nombres": "Felix German", "apellido_paterno": "Flores", "apellido_materno": "Galvez",
        "curp": "FOGF970528HMSLLL04", "email": "germanflores97@outlook.com", "telefono": "527776015185",
        "activo": True
    }
    cliente_id = cliente_test.post(f"{__PREFIJO_URL_CLIENTES}", json=request).json()["respuesta"]["id"]

    response = cliente_test.delete(f"{__PREFIJO_URL_CLIENTES}{cliente_id}")
    assert response.status_code == 200