"""Funciones auxiliares para el ML"""

from functools import lru_cache
from pathlib import Path
from typing import Any

import pickle

from mlhomeserver.ml.utilities.wrappers import SerializableClassifier
import mlhomeserver.settings as settings


@lru_cache(maxsize=300)
def deserialize(filename: str) -> Any:
    """Deserializa un objeto con pickle
    y lo devuelve

    Parameters
    ----------
    filename : str
        _description_

    Returns
    -------
    object
        _description_
    """
    with open(filename, "rb") as f:
        obj = pickle.load(f)
    return obj

@lru_cache(maxsize=500)
def load_model(nombre_desafio: str) -> SerializableClassifier:
    """Carga un modelo serializado de la carpeta
    correspondiente al desafío.
    
    Se necesitará esta función para mostrar los parámetros
    del modelo"""
    nombre_modelo = "".join([nombre_desafio, "_", settings.MODEL_SUFFIX_NAME])
    ruta_modelo = settings.MODELS_FOLDER / Path(nombre_desafio) / nombre_modelo
    modelo: SerializableClassifier = SerializableClassifier.load(ruta_modelo)
    return modelo