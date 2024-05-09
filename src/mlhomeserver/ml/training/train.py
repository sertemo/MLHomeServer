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
import mlhomeserver.config as config


class Training:
    def _setup_parser(self) -> argparse.ArgumentParser:
        """Configura el parser"""
        parser = argparse.ArgumentParser(description="Entrena modelos para desafíos")

        # Añadimos argumentos
        parser.add_argument(
            "desafio",
            help="Nombre del desafío",
            choices=config.CONFIG_DICT.keys(),
            type=str,
        )
        return parser

    def train(self) -> None:
        """Lanza el trainer"""
        # Parseamos los argumentos
        parser = self._setup_parser()
        args = parser.parse_args()

        nombre_desafio = args.desafio
        trainer = Trainer(
            nombre_desafio=nombre_desafio,
            **config.CONFIG_DICT[nombre_desafio],  # TODO Cambiar por dataparser
        )
        try:
            trainer.run()
        except Exception as e:
            print(f"Se ha producido un error al entrenar: {e}")
            return


if __name__ == "__main__":
    Training().train()
