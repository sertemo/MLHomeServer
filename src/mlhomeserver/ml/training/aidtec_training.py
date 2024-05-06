"""Módulo para entrenar el modelo para Aidtec"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from mlhomeserver.ml.training.trainer import Trainer
from ..data_processing.aidtec_transformer import WineDatasetTransformer
import mlhomeserver.settings as settings

nombre = "aidtec"

def train() -> None:
    trainer = Trainer(
        nombre_desafio=nombre,
        dataset=pd.read_csv(settings.DATA_PATH / nombre / "train.csv", index_col=0),
        label_col_name=settings.INFO_DESAFIOS[nombre]['label_col_name'],
        preprocesador=WineDatasetTransformer(
            drop_columns=[
                'year',
                'color',
                'alcohol',
                'densidad',
                'dioxido de azufre libre'
            ]
        ),
        modelo=RandomForestClassifier(
            n_estimators=900
        ),
        label_encoder=True
    )
    trainer.run()

if __name__ == '__main__':
    train()