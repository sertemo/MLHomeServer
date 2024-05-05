"""Módulo del endpoint /about"""

from textwrap import dedent

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ...utils import get_project_version

router = APIRouter(
    responses={
        404: {"mensaje": "No encontrado"}
    },
    tags=["about"]
)

@router.get("/")
async def about():
    return JSONResponse(
        content={"status": "OK",
            "nombre": "ML Home Server",
            "version": get_project_version(),
            "descripción": dedent(
            """
            API para lanzar predicciones de modelos
            de ML previamente entrenados y que corresponden con los desafíos
            de la web de Kopuru.
            """
            )
        }
    )