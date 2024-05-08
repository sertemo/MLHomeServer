"""Módulo para los tests del endpoint /predict"""

from unittest.mock import patch

import numpy as np
import pytest

import mlhomeserver.settings as settings

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
