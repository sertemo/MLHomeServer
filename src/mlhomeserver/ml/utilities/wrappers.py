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

"""Módulo para clases y objetos personalizados válidos
para todos los proyectos de ML"""

import joblib
from pathlib import Path
from typing import cast, Any

import numpy as np
from numpy.typing import NDArray
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin
from sklearn.utils.validation import check_is_fitted


class SerializableMixin:
    """Clase que implementa el método save
    para serializar un modelo"""

    def save(self, model_path: Path) -> None:
        """Serializa el modelo usando joblib"""
        with open(model_path, "wb") as f:
            joblib.dump(self, f)


class DeserializableMixin(SerializableMixin):
    """Clase para cargar y deserializar
    un modelo guardado

    Parameters
    ----------
    SerializableMixin : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    @classmethod
    def load(cls, model_path: str | Path) -> Any:
        with open(model_path, "rb") as f:
            classifier = cast(SerializableClassifier, joblib.load(f))
        return classifier


class SerializableTransformer(BaseEstimator, TransformerMixin, DeserializableMixin):
    """Wrapper de un transformador
    para hacerlo serializable

    Parameters
    ----------
    BaseEstimator : _type_
        _description_
    TransformerMixin : _type_
        _description_
    DeserializableMixin : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    def __init__(self, transformer: TransformerMixin) -> None:
        super().__init__()
        self.transformer = transformer

    def fit(self, y: NDArray[np.float64] | pd.DataFrame) -> "SerializableTransformer":
        self.transformer.fit(y)
        return self

    def transform(self, y: NDArray[np.float64] | pd.DataFrame) -> NDArray[np.int_]:
        check_is_fitted(self.transformer)
        transformation_array: NDArray[np.int_] = self.transformer.transform(y)
        return transformation_array

    def inverse_transform(
        self, y: NDArray[np.float64] | pd.DataFrame
    ) -> NDArray[np.int_]:
        check_is_fitted(self.transformer)
        transformation_array: NDArray[np.int_] = self.transformer.inverse_transform(y)
        return transformation_array

    def __getattr__(self, attr: Any) -> Any:
        """Delega atributos al clasificador subyacente si no se encuentran en 'self'."""
        return getattr(self.transformer, attr)


class SerializableClassifier(
    BaseEstimator,
    ClassifierMixin,
    DeserializableMixin,
):
    """Wrapper de un clasificador para
    que sea serializable y deserializable
    con joblib

    Parameters
    ----------
    BaseEstimator : _type_
        _description_
    ClassifierMixin : _type_
        _description_
    DeserializableMixin : _type_
        _description_
    """

    def __init__(self, classifier: BaseEstimator) -> None:
        self.classifier: BaseEstimator = classifier

    def fit(
        self,
        X: NDArray[np.float64] | pd.DataFrame,
        y: NDArray[np.float64] | pd.DataFrame,
    ) -> "SerializableClassifier":
        self.classifier.fit(X, y)
        return self

    def predict(self, X: NDArray[np.float64] | pd.DataFrame) -> NDArray[np.int64]:
        check_is_fitted(self.classifier)
        predictions: NDArray[np.int64] = self.classifier.predict(X)
        return predictions

    def __getattr__(self, attr: Any) -> Any:
        """Delega atributos al clasificador subyacente si no se encuentran en 'self'."""
        return getattr(self.classifier, attr)
