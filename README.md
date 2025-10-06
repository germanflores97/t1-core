# t1-core

Este proyecto permite la inserción de clientes y tarjetas, ademas de simular cobros realizados y reembolsos.

## Caracteristicas

    - CRUD de clientes
    - CRUD de tarjetas
    - Endpoint para simular cobro, consulta de cobros por cliente y reembolso

## Requisitos para ambientar

Los requisitos para ambientar el proyecto son los siguientes:

    - Python >= 3.13
    - MongoDB >= 8.2

## Instrucciones para instalar

    - Se recomienda crear un entorno virtual de Python con la version sugerida anteriormente (Ejemplo con conda: "conda create -n t1-core python=3.13")
    - Activar el entorno virtual (Ejemplo con conda: "conda activate t1-core")
    - Ir a la raiz del proyecto e instalar las dependencias con "pip install -r src/requirements.txt"
    - Antes del siguiente paso ambientar en el archivo .env la URL de mongodb **Ver el apartado de Consideraciones**
    - Una vez instaladas las dependencias, ejecutar el comando "uvicorn src.app:app --port 8080" para ejecutar la aplicacion en el puerto 8080

## Consideraciones

    - El proyecto esta hecho en FastAPI por lo cual automaticamente genera documentacion en formato OpenAPI, para acceder a ella se puede acceder mediante la url "http://localhost:8080/docs" una vez iniciado el servicio
    - El repositorio cuenta con un archivo .env de prueba en la carpeta src, ahi se deberan configurar las variables externalizadas que se requieran, una de ellas es la url de mongodb
