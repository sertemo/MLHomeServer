"""Módulo del endpoint /about"""

import platform

from datetime import datetime
from textwrap import dedent

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ...utils import get_project_version

router = APIRouter(responses={404: {"mensaje": "No encontrado"}}, tags=["about"])


@router.get("/")
async def about():
    return JSONResponse(
        content={
            "status": "OK",
            "project": {
                "nombre": "ML Home Server",
                "version": get_project_version(),
                "descripción": dedent(
                    """
                API para lanzar predicciones de modelos
                de ML previamente entrenados y que corresponden con los desafíos
                de la web de Kopuru.
                """
                ),
            },
            "server": {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
            },
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }
    )
