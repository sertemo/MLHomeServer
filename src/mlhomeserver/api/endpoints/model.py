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


from fastapi import APIRouter, status

from mlhomeserver.ml.utilities.helpers import load_model_metadata
from mlhomeserver.api.schemas import CustomResponse, ModelInfo
from mlhomeserver.api.utils import validate_competition_or_raise

router = APIRouter(responses={404: {"mensaje": "No encontrado"}}, tags=["model"])


@router.get(
    "/{nombre_desafio}", status_code=status.HTTP_200_OK, response_model=CustomResponse
)
async def detalles_modelo(nombre_desafio) -> CustomResponse:
    # Validamos el nombre de desafío
    validate_competition_or_raise(nombre_desafio)

    # Cargamos la metadata
    metadata = load_model_metadata(nombre_desafio)

    model_info = ModelInfo(
        last_trained=metadata["last_trained"],
        parameters=metadata["params"],
        competition=nombre_desafio,
    )

    response_data = {
        "model_info": model_info.model_dump(),
    }

    return CustomResponse(
        status="OK", data=response_data, message="Información del modelo"
    )
