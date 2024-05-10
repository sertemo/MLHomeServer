"""Módulo para los tests del endpoint /predict"""

from pathlib import Path
from typing import Any
from unittest.mock import patch

import numpy as np
import pytest

from mlhomeserver.exceptions import NonValidPreProcessor, MissingCompetitionFolderError
from mlhomeserver.ml.data_processing.aidtec_transformer import WineDatasetTransformer
from mlhomeserver.ml.predicting.predictor import Predictor
import mlhomeserver.settings as settings
from mlhomeserver.parser import DataParser

@pytest.mark.localtest
def test_predict_with_csv_aidtec_only_local(client):
    try:
        # Abrimos test.csv
        ruta = settings.DATA_PATH / "aidtec" / "test.csv"
        print("ruta archivo", ruta)
        with open(ruta, 'rb') as file:
            response = client.post(
                "/predict/aidtec",
                files={"file": ("filename.csv", file, "text/csv")}
            )
        print("Respuesta content", response.content)
        assert response.status_code == 201
        assert response.json()["status"] == "OK"
        assert "predictions" in response.json()["data"]
    except Exception as e:
        print(f"Error during test execution: {e}")
        print(f"Current DATA_PATH: {settings.DATA_PATH}")
        raise


def test_predict_with_csv_aidtec(client):
    # Prepara un resultado mockeado
    mock_predictions = np.array([5, 6, 5, 5])
    #! OJO: Hay que capturar la función en el módulo en el que es usada !
    with patch('mlhomeserver.api.endpoints.predictions.predict', return_value=mock_predictions):
        try:
            ruta = settings.DATA_PATH / "aidtec" / "test.csv"
            print("ruta archivo", ruta)
            with open(ruta, 'rb') as file:
                response = client.post(
                    "/predict/aidtec",
                    files={"file": ("filename.csv", file, "text/csv")}
                )
            print("Printeando response:", response.json())
            assert response.status_code == 201
            assert response.json()["status"] == "OK"
            assert "predictions" in response.json()["data"]
            # Podrías incluso verificar que las predicciones devueltas sean las esperadas
            assert response.json()["data"]["predictions"]["labels"] == mock_predictions.tolist()

        except Exception as e:
            print(f"Error during test execution: {e}")
            print(f"Current DATA_PATH: {settings.DATA_PATH}")
            raise


def test_predict_with_invalid_file_format(client):
    response = client.post(
        "/predict/aidtec",
        files={"file": ("filename.txt", b"some text content", "text/plain")}
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "Debes enviar un archivo *.csv"


def test_predict_with_csv_wrong_endpoint(client):
    with open(settings.DATA_PATH / "aidtec" / "test.csv", 'rb') as file:
        response = client.post(
            "/predict/none",
            files={"file": ("filename.csv", file, "text/csv")}
        )
    assert response.status_code == 404

def test_predictor_class_init_with_valid_args(aidtec_dataparser):
    from mlhomeserver.settings import LABEL_ENCODER_SUFFIX_NAME, MODEL_SUFFIX_NAME

    p = Predictor(
        nombre_desafio="aidtec",  # Viene del usuario
        dataset="dataframe_Aidtec",  # Viene del usuario
        data_parser=aidtec_dataparser
    )
    assert p.nombre == "aidtec"
    assert p.dataset == "dataframe_Aidtec"
    assert p.label_col_name == "calidad"
    assert isinstance(p.preprocesador, WineDatasetTransformer)
    assert p._nombre_label_encoder == "aidtec_" + LABEL_ENCODER_SUFFIX_NAME
    assert p._nombre_modelo == "aidtec_" + MODEL_SUFFIX_NAME


def test_predictor_class_bad_preprocesor():
    dp = DataParser('aidtec')
    with pytest.raises(NonValidPreProcessor):
        with patch.object(dp, '_load_preprocessor', return_value=object()):
            p = Predictor(
                nombre_desafio="aidtec",  # Viene del usuario
                dataset="dataframe_Aidtec",  # Viene del usuario
                data_parser=dp,
            )
            p.run()

@pytest.mark.localtest
def test_no_folder_model(train_aidtec_raw, aidtec_dataparser):
    p = Predictor(
        nombre_desafio="aidtec",
        dataset=train_aidtec_raw,
        data_parser=aidtec_dataparser
    )

    with patch('mlhomeserver.settings.MODELS_FOLDER', Path('NO_EXISTE')):
        with pytest.raises(MissingCompetitionFolderError):
            p.run()