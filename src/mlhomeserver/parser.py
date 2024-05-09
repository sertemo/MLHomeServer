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

"""Módulo el DataParser que se encarga de extraer info de los desafíos
del archivo YAML y convertirlo a dict para alimentar a Trainer o Predicto"""

import importlib
from typing import Any
import yaml

import pandas as pd
from pathlib import Path
from sklearn.base import TransformerMixin

from mlhomeserver.exceptions import DataConfigError
from mlhomeserver.settings import CONFIG_FILE


class DataParser:
    def __init__(self, challenge_name: str, *, config_path: str = CONFIG_FILE) -> None:
        self.config: dict[str, Any] = self._validate_config_file(
            challenge_name, config_path
        )
        self.challenge_name = challenge_name
        self.dataset_name = self.config["dataset"]["filename"]
        self.label_col_name = self.config["dataset"]["label_col_name"]
        self.root_path = Path("mlhomeserver")

    def _validate_config_file(
        self, challenge_name: str, config_path: str
    ) -> dict[str, Any]:
        """Realiza validación del archivo de configuración de desafíos
        y devuelve el dict correspondiente con el desafío

        Parameters
        ----------
        challenge_name : str
            _description_
        config_path : str
            _description_

        Returns
        -------
        dict[str, str]
            Devuelve el diccionario con los parámetros
            correspondientes al desafío
        """
        try:
            with open(config_path, "r") as file:
                config: dict[str, Any] = yaml.safe_load(file)[challenge_name]
        except yaml.error.YAMLError as e:
            msg = f"Se ha producido un error al acceder al archivo de configuración\
                    {config_path}: {e}"
            print(msg)
            raise DataConfigError(msg)
        except KeyError:
            msg = f"El desafío {challenge_name} no existe."
            print(msg)
            raise DataConfigError(msg)
        except FileNotFoundError:
            msg = f"El archivo de configuración {challenge_name} no existe."
            print(msg)
            raise DataConfigError(msg)
        else:
            return config

    def _get_preprocessor_module(self) -> str:
        preprocessor_module_name = "".join([self.challenge_name, "_", "transformer"])
        return ".".join(
            [self.root_path.name, "ml", "data_processing", preprocessor_module_name]
        )

    def get_train_dataset(self) -> pd.DataFrame:
        self.dataset_path = Path("data") / self.challenge_name / self.dataset_name
        print("path dataset", self.dataset_path)
        params = self.config["dataset"].get("params", dict())
        print("params", params)
        return pd.read_csv(self.dataset_path, **params)

    def get_preprocessor(self) -> TransformerMixin:
        transformer_name = self.config["preprocesador"]["class_name"]
        print("transformer name:", transformer_name)
        preprocessor_module = self._get_preprocessor_module()
        print("módulo preprocesador:", preprocessor_module)
        mod = importlib.import_module(preprocessor_module)
        print("mod", mod)
        preprocessor = getattr(mod, transformer_name)
        params = self.config["preprocesador"].get("params", dict())
        return preprocessor(**params)

    def get_model(self):
        module_name, class_name = self.config["modelo"]["class_name"].rsplit(".", 1)
        mod = importlib.import_module(module_name)
        clazz = getattr(mod, class_name)
        params = self.config["modelo"]["params"]
        return clazz(**params)

    def get_label_encoder(self):
        return self.config["label_encoder"]
