"""Módulo para entrenar modelos y serializarlos"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from sklearn.model_selection import (
    cross_val_score,
    StratifiedKFold,
    cross_val_predict,
)
from sklearn.ensemble import RandomForestClassifier

from ..utilities.wrappers import SerializableClassifier, SerializableTransformer
import settings


def train_aidtec(df_processed: pd.DataFrame, save_filename: str | None = None) -> None:
    """Entrena el mejor modelo del desafío Aidtec con un dataset preprocesado"""

    model = RandomForestClassifier(random_state=42, n_estimators=900)
    model_ser = SerializableClassifier(model)
    try:
        X = df_processed.drop(columns=[settings.AIDTEC_LABEL_COL_NAME])
        y = df_processed[settings.AIDTEC_LABEL_COL_NAME]
    except Exception as e:
        print("Dataset no válido:", {e})

    # Codificamos labels
    label_encoder = LabelEncoder()
    label_encoder_ser = SerializableTransformer(label_encoder)
    y_encoded = label_encoder_ser.fit_transform(y)

    # Evaluamos en cross val
    results_cv = cross_val_score(
        model_ser,
        X,
        y_encoded,
        n_jobs=-1,
        scoring="accuracy",
        cv=StratifiedKFold(n_splits=settings.SPLITS_FOR_CV),
    )

    y_preds = cross_val_predict(
        model_ser,
        X,
        y_encoded,
        cv=StratifiedKFold(n_splits=settings.SPLITS_FOR_CV),
        n_jobs=-1,
    )

    print(f"Resultados de modelo {model_ser.classifier.__class__.__name__}")
    print(
        f"Accuracy media en CV con {settings.SPLITS_FOR_CV} splits: {results_cv.mean():.3%}"
    )
    print(classification_report(y_true=y_encoded, y_pred=y_preds, zero_division=0))

    # Entrenamos
    model_ser.fit(X, y_encoded)

    if save_filename is not None:
        if not save_filename.endswith((".joblib", "pkl")):
            print("El nombre del modelo debe terminar por .pkl o .joblib")
        model_ser.save(settings.MODELS_FOLDER / save_filename)
        label_encoder_ser.save(settings.MODELS_FOLDER / "aidtec_label_encoder.pkl")
