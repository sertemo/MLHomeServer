# Copyright 2024 Sergio Tejedor Moreno

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Funciones auxiliares para el ML"""

from functools import lru_cache
import json
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


def load_model_metadata(nombre_desafio: str) -> dict[str, Any]:
    """Devuelve un dict con la metadata del modelo
    correspondiente al desafío"""
    metadata_filename = "".join([nombre_desafio, "_", settings.MODEL_METADATA_SUFIX])
    ruta_completa = settings.MODELS_FOLDER / Path(nombre_desafio) / metadata_filename

    with open(ruta_completa, "r") as f:
        metadata: dict[str, Any] = json.load(f)

    return metadata
