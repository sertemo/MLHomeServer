# TODO 

import pandas as pd

from mlhomeserver.ml.data_processing.aidtec_transformer import WineDatasetTransformer

def test_corregir_alcohol_type_float(train_aidtec_raw: pd.DataFrame):
    wt = WineDatasetTransformer(
        corregir_alcohol=True,
        corregir_densidad=False,
        color_interactions=False,
        densidad_alcohol_interaction=False,
        ratio_diox=False,
        rbf_diox=False,
        remove_outliers=False,
        standardize=False,
        log_transformation=None,
        drop_columns=None,
        shuffle=False,
    )
    train_transformed = wt.fit_transform(train_aidtec_raw)
    assert train_transformed['alcohol'].dtype == 'float64'