"""Módulo con constantes y rutas generales para el proyecto"""

from pathlib import Path

MODELS_FOLDER = Path('models')
DATA_PATH = Path('data')

# Training
SPLITS_FOR_CV = 5

# Info Desafios
INFO_DESAFIOS = {
    "aidtec": {
        "label_col_name": "calidad"
    }
}
