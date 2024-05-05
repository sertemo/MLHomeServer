"""Módulo con todas las funciones para procesar cada desafío"""

from typing import Literal

import pandas as pd

from .aidtec_transformer import WineDatasetTransformer


def preprocess_aidtec(df: pd.DataFrame, tipo: Literal["train", "test"]) -> pd.DataFrame:
    """Preprocesa el dataset raw del desafío AidTec
    y lo devuelve listo para ser entrenado"""

    # Si pasan el dataset test hay que quitar calidad
    drop_cols = ["year", "color", "alcohol", "densidad", "dioxido de azufre libre"]
    if tipo == "test":
        drop_cols.append("calidad")

    wt = WineDatasetTransformer(drop_columns=["year"])

    df_processed = wt.fit_transform(df)
    return df_processed
