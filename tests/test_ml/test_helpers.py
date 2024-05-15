
import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from unittest.mock import patch

import pytest
import pickle

from mlhomeserver.ml.utilities.helpers import deserialize, load_model_metadata


def test_deserialize():
    # Objeto de prueba
    test_object = {"key": "value", "number": 42}

    # Crear un archivo temporal y serializar el objeto de prueba
    with NamedTemporaryFile(delete=False, mode='wb') as tmp:
        pickle.dump(test_object, tmp)
        tmp_filename = tmp.name  # Guarda el nombre del archivo para usar después

    # Intenta deserializar el objeto del archivo temporal
    try:
        result = deserialize(tmp_filename)
        # Verifica que el objeto deserializado sea igual al original
        assert result == test_object, "El objeto deserializado no coincide con el original"
    finally:
        # Asegúrate de eliminar el archivo temporal después de la prueba
        import os
        os.remove(tmp_filename)



def test_load_model_metadata(tmp_path):
    # Configura los metadatos de prueba
    test_metadata = {
        "last_trained": "ayer",
        "params": {
            "n_estimators": 100,
            "max_depth": 2,
        }
    }
    test_nombre_desafio = "perico"
    test_metadata_suffix = "test_metadata.json"

    metadata_filename = "".join([test_nombre_desafio, "_", test_metadata_suffix])
    ruta_metadata = tmp_path / test_nombre_desafio
    ruta_metadata.mkdir(parents=True, exist_ok=True)
    ruta_completa = ruta_metadata / metadata_filename

    # Serializa los metadatos de prueba en el archivo especificado
    with open(ruta_completa, "w") as f:
        json.dump(test_metadata, f)
    
    # Mockeamos las rutas originales donde se guarda el archivo por las temporales
    with patch('mlhomeserver.ml.utilities.helpers._make_metadata_path', return_value=ruta_completa):
        # Carga los metadatos utilizando la función bajo prueba
        loaded_metadata = load_model_metadata(test_nombre_desafio)
        # Afirmar que los metadatos cargados son iguales a los metadatos guardados
        assert loaded_metadata == test_metadata, "Los metadatos cargados no coinciden con los metadatos guardados"
