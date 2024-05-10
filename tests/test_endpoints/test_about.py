

def test_predict_with_csv_aidtec(client):
    # Prepara un resultado mockeado
    response = client.get(
            "/about",
        )
    print("Printeando response:", response.json())
    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    assert response.json()["autor"]["nombre"] == "Sergio Tejedor"