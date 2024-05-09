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

"""Módulo que recoge la clase Predictor general"""

import numpy as np
from numpy.typing import NDArray
from pathlib import Path

import pandas as pd

from mlhomeserver.ml.utilities.wrappers import (
    SerializableClassifier,
    SerializableTransformer,
)
from mlhomeserver.exceptions import PreProcessorError, MissingCompetitionFolderError
from mlhomeserver.ml.utilities.helpers import load_model
import mlhomeserver.settings as settings
from mlhomeserver.parser import DataParser


class Predictor:
    """Clase general para predecir"""

    def __init__(
        self,
        nombre_desafio: str,
        dataset: pd.DataFrame,
        data_parser: DataParser,
    ) -> None:
        self.nombre = nombre_desafio
        self.dataset = dataset
        self.dp = data_parser
        self.label_col_name = data_parser.label_col_name
        self.preprocesador = data_parser.get_preprocessor()
        self._nombre_modelo = "".join([self.nombre, "_", settings.MODEL_SUFFIX_NAME])
        self._nombre_label_encoder = "".join(
            [self.nombre, "_", settings.LABEL_ENCODER_SUFFIX_NAME]
        )

    def run(self) -> None:
        """Ejecuta la Pipeline de preproceso
        y predicciones deserializando el modelo
        y el label encoder en caso de que
        haya"""

        # Preprocesamos
        try:
            df_preprocessed: pd.DataFrame = self.preprocesador.fit_transform(
                self.dataset
            )
        except Exception as e:
            raise PreProcessorError(f"Se ha producido un error al preprocesar: {e}")

        # Quitamos la columna de los labels
        X_test = df_preprocessed.drop(columns=[self.label_col_name])

        # Verificamos que exista carpeta del desafío
        self.carpeta_modelo = settings.MODELS_FOLDER / Path(self.nombre)
        if not self.carpeta_modelo.exists():
            raise MissingCompetitionFolderError(
                f"No existe la carpeta {self.carpeta_modelo}.\
                                                Modelo no serializado."
            )

        # Deserializamos el modelo
        self.modelo: SerializableClassifier = load_model(self.nombre)

        # Lanzamos las predicciones
        self.preds: NDArray[np.int_] = self.modelo.predict(X_test)

        # Comprobamos si hay label encoders
        ruta_label_encoder = (
            settings.MODELS_FOLDER / Path(self.nombre) / self._nombre_label_encoder
        )
        if ruta_label_encoder.exists():
            label_encoder: SerializableTransformer = SerializableTransformer.load(
                ruta_label_encoder
            )
            # Descodificamos las predicciones
            self.preds = label_encoder.inverse_transform(self.preds)
