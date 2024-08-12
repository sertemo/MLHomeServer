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

"""Módulo con la clase Trainer General válida para entrenar cualquier modelo"""

from datetime import datetime
import json
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

from mlhomeserver.exceptions import (
    PreProcessorError,
)
from mlhomeserver.ml.utilities.wrappers import (
    SerializableClassifier,
    SerializableTransformer,
)
import mlhomeserver.settings as settings


class Trainer:
    def __init__(
        self,
        nombre_desafio: str,
        train_dataset: pd.DataFrame,
        label_col_name: str,
        preprocesador: TransformerMixin,
        modelo: ClassifierMixin,
        label_encoder: bool = False,
        train_dataset_index_col: int = 0,
    ) -> None:
        self.nombre = nombre_desafio
        self.train_dataset = train_dataset
        self.label_col_name = label_col_name
        self.preprocesador = preprocesador
        self.modelo = modelo
        self.label_encoder = label_encoder
        self.index_col = train_dataset_index_col

    def __repr__(self) -> str:
        return f"""{self.__class__.__name__}(nombre={self.nombre},
        label_col_name={self.label_col_name}, preprocesador={self.preprocesador},
        modelo={self.modelo}, label_encoder={self.label_encoder},
        train_dataset_index_col={self.index_col},
        label_encoder={self.label_encoder},
        dataset_columns={self.train_dataset.columns})"""

    def _preprocess(self, X: pd.DataFrame, y: pd.DataFrame) -> pd.DataFrame:
        """Ejecuta el preprocesamiento

        Returns
        -------
        pd.DataFrame
            _description_
        """
        try:
            X_preprocessed = self.preprocesador.fit_transform(X, y)
        except Exception as e:
            raise PreProcessorError(e)
        return X_preprocessed

    def _save_model_metadata(
        self, modelo_desafio_folder: Path, modelo: SerializableClassifier
    ) -> None:
        """Guarda en un json la metadata del modelo:
        el last_trained y los parámetros
        """
        metadata_path = modelo_desafio_folder / (
            self.nombre + "_" + settings.MODEL_METADATA_SUFIX
        )
        metadata = {
            "last_trained": str(datetime.now().isoformat()),
            "params": modelo.get_params(),
        }
        print("Metadata:", metadata)

        with open(metadata_path, "w") as f:
            json.dump(metadata, f)

    def run(self) -> None:
        """Ejecuta la Pipeline de preproceso
        y entrenamiento guardando el modelo
        y el label encoder en caso de haberlo"""
        start = time.perf_counter()

        # Separamos X_train y_train
        X_train = self.train_dataset.drop(columns=[self.label_col_name])
        y_train = self.train_dataset[self.label_col_name]

        # Preprocesamos
        try:
            X_train = self._preprocess(X_train, y_train)
            # Verificamos si ha habido cambio de índices
            if hasattr(self.preprocesador, "y_index"):
                y_train = y_train.reindex(self.preprocesador.y_index)
                print("Despues de reindexar:")
                print(y_train.index)
        except Exception as e:
            raise PreProcessorError(f"Se ha producido un error al preprocesar: {e}")

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
        print(f"Resultados del modelo {self.modelo.__class__.__name__}")
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
        self.modelo.save(
            modelo_desafio_folder / (self.nombre + "_" + settings.MODEL_SUFFIX_NAME)
        )
        if self.label_encoder:
            label_encoder.save(
                modelo_desafio_folder
                / (self.nombre + "_" + settings.LABEL_ENCODER_SUFFIX_NAME)
            )

        # Guardamos la metadata
        self._save_model_metadata(modelo_desafio_folder, self.modelo)

        # Fin del contador
        end = time.perf_counter()

        # Calcular el tiempo total en segundos
        elapsed_time = end - start

        # Convertir segundos a minutos y segundos
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)

        print(
            f"Entrenamiento terminado. Tiempo de ejecución: {minutes} minutos y {seconds} segundos"
        )
        print(f"Guardado modelo y metadata en {modelo_desafio_folder}")
        if self.label_encoder:
            print(f"Guardado LabelEncoder en {modelo_desafio_folder}")
