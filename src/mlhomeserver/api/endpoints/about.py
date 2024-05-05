"""Módulo del endpoint about"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix='/about',
    responses={
        404: {"mensaje": "No encontrado"}
    },
    tags=["about"]
)

@router.get("/")
async def about():
    return JSONResponse(
        content={"status": "OK",
            "msg": "La app funciona correctamente",
            "predicciones": {
                "endpoint": "/predict",
                "requisitos": "Envía un csv para predecir",
                "csv": "El csv debe corresponder al reto AidTec de kopuru",
            }
        }
    )