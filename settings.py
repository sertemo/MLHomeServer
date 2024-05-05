"""Módulo con constantes y rutas generales para el proyecto"""

from pathlib import Path

MODELS_FOLDER = Path('models')
MODELO_PATH = MODELS_FOLDER / 'wine_random_forest_STM.pkl'
LABEL_ENCODER_PATH = MODELS_FOLDER / 'wine_label_encoder.pkl'

# Training

SPLITS_FOR_CV = 5
# Labels
AIDTEC_LABEL_COL_NAME = 'calidad'