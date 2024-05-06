"""Módulo con las diferentes configuraciones de cada desafío"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier

import mlhomeserver.settings as settings
from mlhomeserver.ml.data_processing.aidtec_transformer import WineDatasetTransformer

DESAFIOS = {
    "aidtec": {
        "label_col_name": "calidad",
        "dataset": pd.read_csv(settings.DATA_PATH / "aidtec" / "train.csv", index_col=0),
        "preprocesador": WineDatasetTransformer(
            drop_columns=[
                'year',
                'color',
                'alcohol',
                'densidad',
                'dioxido de azufre libre'
            ]
        ),
        "modelo": RandomForestClassifier(
            n_estimators=900,
            random_state=42
        ),
        "label_encoder": True
    },
}