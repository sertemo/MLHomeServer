#!/usr/bin/env python

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

"""Módulo que ejecuta la lógica de entrenamiento"""

import argparse

from mlhomeserver.ml.training.trainer import Trainer
from mlhomeserver.parser import DataParser
from mlhomeserver.utils import get_current_competitions_from_yml
from mlhomeserver.logging_config import logger


class Training:
    def _setup_parser(self) -> argparse.ArgumentParser:
        """Configura el parser"""
        parser = argparse.ArgumentParser(description="Entrena modelos para desafíos")

        # Añadimos argumentos
        parser.add_argument(
            "desafio",
            help="Nombre del desafío",
            choices=get_current_competitions_from_yml(),
            type=str,
        )
        return parser

    def train(self) -> None:
        """Lanza el trainer"""
        # Parseamos los argumentos
        parser = self._setup_parser()
        args = parser.parse_args()

        nombre_desafio = args.desafio

        # Instanciamos el dataparser
        dp = DataParser(nombre_desafio)

        trainer = Trainer(
            nombre_desafio=nombre_desafio,
            train_dataset=dp.get_train_dataset(),
            label_col_name=dp.label_col_name,
            preprocesador=dp.get_preprocessor(),
            modelo=dp.get_model(),
            label_encoder=dp.get_label_encoder(),
        )
        try:
            trainer.run()
            logger.info(f"Entrenamiento de {nombre_desafio} realizado correctamente.")
        except Exception as e:
            logger.error(f"Se ha producido un error al entrenar: {e}")
            print(e)
            return


if __name__ == "__main__":
    Training().train()
