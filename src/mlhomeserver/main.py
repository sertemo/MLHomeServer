# Copyright 2024 Sergio Tejedor Moreno

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Entry point principal de la app"""
from contextlib import asynccontextmanager
from typing import Callable, Awaitable, Any

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from mlhomeserver.api.routers import main_router
from mlhomeserver.logging_config import logger
from mlhomeserver.settings import LOG_PATH

app = FastAPI()

app.include_router(main_router)


@asynccontextmanager
async def lifespan(app):
    # Lo que va antes del yield se ejecuta en el startup
    if not LOG_PATH.exists():
        LOG_PATH.touch()
    logger.info("** Aplicación iniciada **")
    yield
    # Lo que viene ahora se ejecuta al finalizar la aplicación
    logger.info("** Aplicación terminada **")


# Creamos middleware para capturar info de las solicitudes
@app.middleware("http")
async def log_requests(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Any:
    # Obtener la IP del cliente de X-Forwarded-For o request.client
    client_ip = request.headers.get("X-Forwarded-For")
    if not client_ip:
        client_ip = request.client.host if request.client else "Unknown"

    logger.info(f"Request: {request.method} {request.url} de {client_ip}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


@app.get("/")
async def root() -> JSONResponse:
    return JSONResponse(content={"ML Home Server": "STM 2024"})


if __name__ == "__main__":
    pass
