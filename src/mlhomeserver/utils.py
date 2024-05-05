"""Funciones auxiliares generales para todo el proyecto"""

import toml

def get_project_version() -> str:
    """Devuelve la versión del proyecto
    extraido del pyproject.toml"""
    with open('pyproject.toml', 'r') as file:
        data = toml.load(file)
    return data['tool']['poetry']['version']