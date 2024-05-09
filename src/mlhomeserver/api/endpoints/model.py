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

"""Router para mostrar los parámetros de los modelos entrenados"""

from datetime import datetime

from fastapi import APIRouter, status

from mlhomeserver.ml.utilities.helpers import load_model
from mlhomeserver.ml.utilities.wrappers import SerializableClassifier
from mlhomeserver.api.schemas import CustomResponse, ModelInfo

router = APIRouter(responses={404: {"mensaje": "No encontrado"}}, tags=["predict"])


@router.get(
    "/{nombre_desafio}", status_code=status.HTTP_200_OK, response_model=CustomResponse
)
async def detalles_modelo(nombre_desafio):
    # Cargamos el modelo
    modelo: SerializableClassifier = load_model(nombre_desafio)
    model_info = ModelInfo(
        last_trained=datetime(2024, 5, 1),
        parameters=modelo.get_params(),
        competition=nombre_desafio,
    )

    response_data = {
        "model_info": model_info.model_dump(),
    }

    return CustomResponse(
        status="OK", data=response_data, message="Información del modelo"
    )
