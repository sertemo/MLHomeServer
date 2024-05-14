from datetime import datetime

import pytest

from mlhomeserver.utils import get_current_competitions_from_yml
from mlhomeserver.api.schemas import CustomResponse

def test_model_with_invalid_competition_name(client):
    response = client.get(
        "/model/no_existe",
    )
    assert response.status_code == 404
    print("Printeando response:", response.json())
    assert response.json() == {"detail": f"El nombre de desafío no_existe no es un desafío válido.\
            Los desafíos válidos son: {', '.join(get_current_competitions_from_yml())}"}


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