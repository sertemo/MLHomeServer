"""Funciones auxiliares generales para todo el proyecto"""

from typing import Any

import toml


def get_project_version() -> str:
    """Devuelve la versión del proyecto
    extraido del pyproject.toml"""
    with open("pyproject.toml", "r") as file:
        data: dict[str, Any] = toml.load(file)
        version: str = data["tool"]["poetry"]["version"]
    return version
