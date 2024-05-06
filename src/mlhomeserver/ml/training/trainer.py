"""Módulo con la clase Trainer General válida para entrenar cualquier modelo"""

from pathlib import Path
import time

import pandas as pd
from sklearn.base import ClassifierMixin, TransformerMixin
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from sklearn.model_selection import (
    cross_val_score,
    StratifiedKFold,
    cross_val_predict,
)

from mlhomeserver.ml.utilities.wrappers import SerializableClassifier, SerializableTransformer
import mlhomeserver.settings as settings


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
        start = time.perf_counter()

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
        print("Evaluando el modelo ...")
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
        print("Entrenando el modelo ...")
        self.modelo = SerializableClassifier(self.modelo)
        self.modelo.fit(X_train, y_train)

        # Guardamos el modelo y label encoder en caso de haber
        # Creamos el folder por si no existe
        modelo_desafio_folder = settings.MODELS_FOLDER / Path(self.nombre)
        modelo_desafio_folder.mkdir(exist_ok=True)
        self.modelo.save(modelo_desafio_folder / (self.nombre + "_" + "model.joblib"))
        if self.label_encoder:
            label_encoder.save(modelo_desafio_folder / (self.nombre + "_" + "labelencoder.joblib"))

        # Fin del contador
        end = time.perf_counter()

        # Calcular el tiempo total en segundos
        elapsed_time = end - start

        # Convertir segundos a minutos y segundos
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)

        print(f"Entrenamiento terminado. Tiempo de ejecución: {minutes} minutos y {seconds} segundos")
        print(f"Guardado modelo en {modelo_desafio_folder}")
        if self.label_encoder:
            print(f"Guardado LabelEncoder en {modelo_desafio_folder}")
