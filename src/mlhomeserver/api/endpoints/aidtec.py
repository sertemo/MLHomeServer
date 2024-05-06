"""Módulo para el endpoint del desafio AidTec"""

from datetime import datetime

from fastapi import APIRouter
from fastapi import File, UploadFile, HTTPException, status
import numpy as np
from numpy.typing import NDArray
import pandas as pd
from sklearn.preprocessing import LabelEncoder

from ...schemas import Prediction, PredictionResponse, ModelInfo
from ...ml.utilities.wrappers import SerializableClassifier
from ...ml.utilities.helpers import deserialize
import settings


router = APIRouter(
    responses={404: {"mensaje": "No encontrado"}}, tags=["predict"]
)


@router.post(
    "/predict", status_code=status.HTTP_201_CREATED, response_model=PredictionResponse
)
async def predicciones(file: UploadFile = File(...)):
    try:
        if file.filename and file.filename.endswith(".csv"):  # TODO: Cambiar todo esto
            # Convierte el archivo cargado en un DataFrame
            data_frame = pd.read_csv(file.file, index_col=0)
            # Cargamos el modelo y los label encoders
            modelo: SerializableClassifier = deserialize(settings.MODELO_PATH)
            label_encoder: LabelEncoder = deserialize(settings.LABEL_ENCODER_PATH)
            # Lanzamos las predicciones
            predictions: NDArray[np.int_] = modelo.predict(data_frame)
            preds_decoded: NDArray[np.int_] = label_encoder.inverse_transform(
                predictions
            )

            final_preds = Prediction(
                labels=preds_decoded.tolist(), length=len(preds_decoded)
            )

            response_data = {
                "predictions": final_preds,
            }

            return PredictionResponse(
                status="OK",
                data=response_data,
                message="Predicciones realizadas con éxito",
            )

        else:
            return {"error": "Formato no válido. Debes enviar un *.csv"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/model", status_code=status.HTTP_200_OK, response_model=ModelInfo
)
async def detalles_modelo():

    return ModelInfo(
                last_trained=datetime(2024, 5, 1),
                parameters= {"n_estimators": 900}  #modelo.get_params()
            )