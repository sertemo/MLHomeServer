"""Módulo con constantes y rutas generales para el proyecto"""

from pathlib import Path

MODELS_FOLDER = Path("models")
DATA_PATH = Path("data")
MODEL_SUFFIX_NAME = "model.joblib"
LABEL_ENCODER_SUFFIX_NAME = "labelencoder.joblib"

# Training
SPLITS_FOR_CV = 5
