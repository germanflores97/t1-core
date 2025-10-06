from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.clientes.routes import clientes_router
from src.commons.exceptions import BusinessException
from src.commons.schemas import GenericResponse

app = FastAPI()
app.title = "t1-core"
app.version = "0.1"

@app.middleware("http")
async def http_error_handler(request: Request, call_next) -> Response:
    try:
        return await call_next(request)
    except BusinessException as error:
        print(f"\033[91mError: {error}\033[0m") #TODO: Implementar logger
        return JSONResponse(GenericResponse(mensaje=error.mensaje).model_dump(), status_code=error.codigo)
    except Exception as error:
        print(f"\033[91mError no controlado: {error}\033[0m") #TODO: Implementar logger
        return JSONResponse(GenericResponse(mensaje="Error no controlado").model_dump(), status_code=500)
    
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    primer_mensaje_error = ""

    for error in exc.errors(): #TODO: Buscar la forma de imprimir el nombre de campo faltante
        primer_mensaje_error = error["msg"]
        break

    print(f"\033[91mError de validación: {primer_mensaje_error}\033[0m") #TODO: Implementar logger
    return JSONResponse(
        status_code=422,
        content=GenericResponse(mensaje=primer_mensaje_error).model_dump(),
    )

app.include_router(router=clientes_router, prefix="/clientes")