from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from src.clientes.routes import clientes_router
from src.tarjetas.routes import tarjetas_router
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

app.include_router(router=clientes_router, prefix="/clientes")
app.include_router(router=tarjetas_router, prefix="/tarjetas")