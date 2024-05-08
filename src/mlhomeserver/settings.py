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

"""Módulo con constantes y rutas generales para el proyecto"""

from pathlib import Path

# Esto asumirá que DATA_PATH debe ser un directorio relativo al directorio del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data"
MODELS_FOLDER = BASE_DIR / "models"
MODEL_SUFFIX_NAME = "model.joblib"
LABEL_ENCODER_SUFFIX_NAME = "labelencoder.joblib"

# Training
SPLITS_FOR_CV = 5
