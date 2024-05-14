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

"""Módulo para recoger funciones auxiliares de la API"""

from fastapi import HTTPException, status

from mlhomeserver.utils import get_current_competitions_from_yml


def validate_competition_or_raise(nombre_desafio: str) -> None:
    """Valida que un determinado desafio sea válido,
    sino lanza excepcion HTTP

    Parameters
    ----------
    nombre_desafio : str
        _description_

    Raises
    ------
    HTTPException
        _description_
    """
    if nombre_desafio not in get_current_competitions_from_yml():
        print(f"Nombre de desafío no válido: {nombre_desafio}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El nombre de desafío {nombre_desafio} no es un desafío válido.\
            Los desafíos válidos son: {', '.join(get_current_competitions_from_yml())}",
        )
