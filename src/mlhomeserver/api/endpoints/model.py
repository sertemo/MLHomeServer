"""Router para mostrar los parámetros de los modelos entrenados"""

from datetime import datetime

from fastapi import APIRouter, status

from mlhomeserver.ml.utilities.helpers import load_model
from mlhomeserver.ml.utilities.wrappers import SerializableClassifier
from mlhomeserver.schemas import CustomResponse, ModelInfo

router = APIRouter(responses={404: {"mensaje": "No encontrado"}}, tags=["predict"])

@router.get("/{nombre_desafio}", status_code=status.HTTP_200_OK, response_model=CustomResponse)
async def detalles_modelo(nombre_desafio):
    # Cargamos el modelo
    modelo: SerializableClassifier = load_model(nombre_desafio)
    model_info = ModelInfo(
        last_trained=datetime(2024, 5, 1),
        parameters=modelo.get_params(),
        competition=nombre_desafio
    )

    response_data = {
        "model_info": model_info.model_dump(),
    }
    
    return CustomResponse(
        status="OK",
        data=response_data,
        message="Información del modelo"
    )