"""Módulo para el endpoint del desafio AidTec"""

from fastapi import APIRouter
from fastapi import File, UploadFile, HTTPException, status
import pandas as pd


from mlhomeserver.ml.predicting.predict import predict
from ...schemas import CustomResponse, Prediction

router = APIRouter(responses={404: {"mensaje": "No encontrado"}}, tags=["predict"])


@router.post(
    "/{nombre_desafio}", status_code=status.HTTP_201_CREATED, response_model=CustomResponse
)
async def predicciones(nombre_desafio:str, file: UploadFile = File(...)):
    try:
        if file.filename and file.filename.endswith(".csv"):
            # Convierte el archivo cargado en un DataFrame
            data_frame = pd.read_csv(file.file, index_col=0)

            preds = predict(
                nombre_desafio=nombre_desafio,
                dataset_predecir=data_frame
            )

            preds_response = Prediction(labels=preds.tolist(), length=len(preds))

            response_data = {
                "predictions": preds_response,
            }

            return CustomResponse(
                status="OK",
                data=response_data,
                message="Predicciones realizadas con éxito",
            )

        else:
            return {"error": "Formato no válido. Debes enviar un *.csv"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
