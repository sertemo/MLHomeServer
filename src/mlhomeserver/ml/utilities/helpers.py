"""Funciones auxiliares para el ML"""

from functools import lru_cache
from typing import Any

import pickle


@lru_cache(maxsize=300)
def deserialize(filename: str) -> Any:
    """Deserializa un objeto con pickle
    y lo devuelve

    Parameters
    ----------
    filename : str
        _description_

    Returns
    -------
    object
        _description_
    """
    with open(filename, "rb") as f:
        obj = pickle.load(f)
    return obj
