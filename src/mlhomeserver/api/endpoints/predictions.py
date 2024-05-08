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

"""Módulo para el endpoint de predicciones. Debe intentar ser válido
para todos los desafíos"""

from fastapi import APIRouter
from fastapi import File, UploadFile, HTTPException, status
import pandas as pd


from mlhomeserver.ml.predicting.predict import predict
import mlhomeserver.config as config
from mlhomeserver.schemas import CustomResponse, Prediction

router = APIRouter(responses={404: {"error": "No encontrado"}})


@router.post(
    "/{nombre_desafio}",
    status_code=status.HTTP_201_CREATED,
    response_model=CustomResponse,
)
async def predicciones(nombre_desafio: str, file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith(".csv"):
        print(f"Archivo no válido: {nombre_desafio}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Debes enviar un archivo *.csv",
        )

    if nombre_desafio not in config.CONFIG_DICT:
        print(f"Nombre de desafío no válido: {nombre_desafio}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El nombre de desafío {nombre_desafio} no es un desafío válido. \
                Los desafíos válidos son: {list(config.CONFIG_DICT)}",
        )

    # Abrimos el dataframe
    # La primera columna es el índice
    try:
        data_frame = pd.read_csv(file.file, index_col=0)
    except pd.errors.EmptyDataError as e:
        print("DEBUG:", e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"El archivo CSV está vacío: {e}",
        )
    except pd.errors.ParserError as e:
        print("DEBUG:", e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error al parsear el CSV: {e}",
        )
    except Exception as e:
        print("DEBUG:", e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error desconocido al cargar CSV: {e}",
        )

    # Lanzamos predicciones
    try:
        preds = predict(nombre_desafio=nombre_desafio, dataset_predecir=data_frame)
    except Exception as e:
        print("DEBUG:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producid un error al predecir: {e}",
        )
    else:
        preds_response = Prediction(labels=preds.tolist(), length=len(preds))

    response_data = {
        "predictions": preds_response,
    }

    return CustomResponse(
        status="OK",
        data=response_data,
        message="Predicciones realizadas con éxito",
    )
