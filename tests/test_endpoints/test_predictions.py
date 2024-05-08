"""Módulo para los tests del endpoint /predict"""


import mlhomeserver.settings as settings

def test_predict_with_csv_aidtec(client):
    try:
        # Suponiendo que 'example.csv' es un archivo válido para pruebas
        with open(settings.DATA_PATH / "aidtec" / "test.csv", 'rb') as file:
            response = client.post(
                "/predict/aidtec",
                files={"file": ("filename.csv", file, "text/csv")}
            )
        assert response.status_code == 201
        assert response.json()["status"] == "OK"
        assert "predictions" in response.json()["data"]
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
    # Suponiendo que 'example.csv' es un archivo válido para pruebas
    with open(settings.DATA_PATH / "aidtec" / "test.csv", 'rb') as file:
        response = client.post(
            "/predict/none",
            files={"file": ("filename.csv", file, "text/csv")}
        )
    assert response.status_code == 404
