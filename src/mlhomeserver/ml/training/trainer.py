"""Módulo con la clase Trainer General válida para entrenar cualquier modelo"""

import pandas as pd
from sklearn.base import ClassifierMixin, TransformerMixin
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from sklearn.model_selection import (
    cross_val_score,
    StratifiedKFold,
    cross_val_predict,
)

from ..utilities.wrappers import SerializableClassifier, SerializableTransformer
import settings


class Trainer:
    def __init__(
            self,
            nombre_desafio: str,
            dataset: pd.DataFrame,
            label_col_name: str,
            preprocesador: TransformerMixin,
            modelo: ClassifierMixin,
            label_encoder: bool = False
            ) -> None:
        self.nombre = nombre_desafio
        self.dataset = dataset
        self.label_col_name = label_col_name
        self.preprocesador = preprocesador
        self.modelo = modelo
        self.label_encoder = label_encoder

    def run(self) -> None:
        """Ejecuta la Pipeline de preproceso
        y entrenamiento guardando el modelo
        y el label encoder en caso de haberlo"""
        # Preprocesamos
        df_preprocessed: pd.DataFrame = self.preprocesador.fit_transform(self.dataset)

        # Separamos X_train y_train
        X_train = df_preprocessed.drop(columns=[self.label_col_name])
        y_train = df_preprocessed[self.label_col_name]
        if self.label_encoder:
            label_encoder = LabelEncoder()
            label_encoder = SerializableTransformer(label_encoder)
            y_train = label_encoder.fit_transform(y_train)

        # Evaluamos en CV
        # Evaluamos en cross val
        results_cv = cross_val_score(
            self.modelo,
            X_train,
            y_train,
            scoring="accuracy",
            cv=StratifiedKFold(n_splits=settings.SPLITS_FOR_CV),
        )

        y_preds = cross_val_predict(
            self.modelo,
            X_train,
            y_train,
            cv=StratifiedKFold(n_splits=settings.SPLITS_FOR_CV),
        )
        print(f"Resultados de modelo {self.modelo.__class__.__name__}")
        print(
            f"Accuracy media en CV con {settings.SPLITS_FOR_CV} splits: {results_cv.mean():.3%}"
        )
        print(classification_report(y_true=y_train, y_pred=y_preds, zero_division=0))

        # Entrenamos el modelo
        # Serializamos con el wrapper
        self.modelo = SerializableClassifier(self.modelo)
        self.modelo.fit(X_train, y_train)

        # Guardamos el modelo y label encoder en caso de haber
        self.modelo.save(settings.MODELS_FOLDER / self.nombre + "_" + "model.joblib")
        if self.label_encoder:
            label_encoder.save(settings.MODELS_FOLDER / self.nombre + "_" + "labelencoder.joblib")

        print("Entrenamiento finalizado con éxito")
