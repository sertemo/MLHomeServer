from datetime import datetime

from fastapi import HTTPException
import pytest

from mlhomeserver.utils import get_current_competitions_from_yml
from mlhomeserver.api.schemas import CustomResponse

def test_model_with_invalid_competition_name(client):
    response = client.get(
        "/model/no_existe",
    )
    assert response.status_code == 404
    response_json = response.json()
    print("Printeando response:", response.json())
    assert "error" in response_json["detail"]
    assert "válidos" in response_json["detail"]


@pytest.mark.localtest
def test_model_with_valid_name(client):
    response = client.get(
        "/model/aidtec",
    )
    assert response.status_code == 200
    response_dict = response.json()
    print(response_dict)
    assert 'last_trained' in response_dict['data']['model_info']
    fecha_isoformat = response_dict['data']['model_info']['last_trained']
    assert isinstance(datetime.fromisoformat(fecha_isoformat), datetime)


def test_detalles_modelo_success(mocker, client):
    # Configuración de los mocks
    mock_metadata = {
        "last_trained": "2021-06-01T12:00:00",
        "params": {"n_estimators": 100, "max_depth": 2}
    }
    mocker.patch("mlhomeserver.api.endpoints.model.validate_competition_or_raise")
    mocker.patch("mlhomeserver.api.endpoints.model.load_model_metadata", return_value=mock_metadata)
    
    # Llamada al endpoint
    response = client.get("/model/aidtec")

    # Verificación
    assert response.status_code == 200
    response_json = response.json()
    print(response_json)
    assert response_json["status"] == "OK"
    assert response_json["data"]["model_info"]["last_trained"] == "2021-06-01T12:00:00"
    assert response_json["data"]["model_info"]["parameters"] == {"n_estimators": "100", "max_depth": "2"}


def test_detalles_modelo_failure(mocker, client):
    # Configuración de los mocks para simular una validación fallida
    mocker.patch("mlhomeserver.api.endpoints.model.validate_competition_or_raise", side_effect=HTTPException(status_code=404, detail="No encontrado"))

    # Llamada al endpoint
    response = client.get("/model/invalid_competition")

    # Verificación
    assert response.status_code == 404
    assert response.json() == {"detail": "No encontrado"}