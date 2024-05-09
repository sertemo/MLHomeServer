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

"""Funciones auxiliares generales para todo el proyecto"""

import toml
from typing import Any
import yaml

from mlhomeserver.settings import CONFIG_FILE


def get_project_version() -> str:
    """Devuelve la versión del proyecto
    extraido del pyproject.toml"""
    with open("pyproject.toml", "r") as file:
        data: dict[str, Any] = toml.load(file)
        version: str = data["tool"]["poetry"]["version"]
    return version


def get_current_competitions_from_yml() -> list[str]:
    """Devuelve los nombres de los desafios
    del archivo de configuracion de los yml

    Returns
    -------
    list
        _description_
    """
    with open(CONFIG_FILE, "r") as file:
        archivo_config: dict[str, Any] = yaml.safe_load(file)
    return list(archivo_config.keys())
