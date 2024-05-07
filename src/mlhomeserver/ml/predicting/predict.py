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

"""Módulo que ejecuta la lógica de predicción"""

import numpy as np
from numpy.typing import NDArray
import pandas as pd

from mlhomeserver.ml.predicting.predictor import Predictor
import mlhomeserver.config as dsettings


def predict(nombre_desafio: str, dataset_predecir: pd.DataFrame) -> NDArray[np.int_]:
    """Devuelve las predicciones utilizando el Predictor"""
    predictor = Predictor(
        nombre_desafio=nombre_desafio,
        dataset=dataset_predecir,
        label_col_name=dsettings.CONFIG_DICT[nombre_desafio]["label_col_name"],
        preprocesador=dsettings.CONFIG_DICT[nombre_desafio]["preprocesador"],
    )
    predictor.run()

    return predictor.preds


if __name__ == "__main__":
    pass
