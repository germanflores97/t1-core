from pathlib import Path
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from src.core.logger_config import logger

from src.clientes.routes import clientes_router
from src.tarjetas.routes import tarjetas_router
from src.cobros.routes import cobros_router
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
        logger.error(error.mensaje)
        return JSONResponse(GenericResponse(mensaje=error.mensaje).model_dump(), status_code=error.codigo)
    except Exception as error:
        logger.error(str(error), exc_info=True)
        return JSONResponse(GenericResponse(mensaje="Error no controlado").model_dump(), status_code=500)

app.include_router(router=clientes_router, prefix="/clientes")
app.include_router(router=tarjetas_router, prefix="/tarjetas")
app.include_router(router=cobros_router, prefix="/cobros")