import json

import pandas as pd
import pytest
from unittest.mock import MagicMock, patch

from mlhomeserver.ml.training.train import Training
from mlhomeserver.ml.training.trainer import Trainer
from mlhomeserver.exceptions import PreProcessorError
from mlhomeserver import settings


def test_trainer_bad_preprocessor_aidtec(trainer_bad_preprocessor):
    with pytest.raises(PreProcessorError):
        trainer_bad_preprocessor.run()


def test_train_function_calls_run(mock_trainer):
    trainer_mock = mock_trainer.return_value
    trainer_mock.run.return_value = 'Mocked'

    t = Training()
    t._setup_parser = MagicMock()
    t._setup_parser().parse_args.return_value = MagicMock(desafio='aidtec')

    t.train()

    trainer_mock.run.assert_called_once()


def test_save_model_metadata(tmp_path, mock_model):
    # Preparar el directorio donde se guardarán los metadatos
    tmp_path.mkdir(parents=True, exist_ok=True)
    
    # Ejecutar el método a probar
    trainer = Trainer(
        nombre_desafio="aidtec",
        label_col_name="calidad",
        train_dataset="train.csv",
        preprocesador=object(),
        modelo=object(),
        label_encoder=True,
    )
    trainer._save_model_metadata(tmp_path, mock_model)
    
    # Construir la ruta esperada del archivo JSON
    expected_path = tmp_path / f"aidtec_{settings.MODEL_METADATA_SUFIX}"
    
    # Asegurar que el archivo existe
    assert expected_path.exists(), "El archivo de metadatos no fue creado"
    
    # Leer y verificar el contenido del archivo
    with open(expected_path, 'r') as f:
        metadata = json.load(f)
    
    assert metadata['last_trained'], "El timestamp de last_trained está vacío o ausente"
    assert metadata['params'] == {'n_estimators': 100, 'max_depth': 2}, "Los parámetros no coinciden con los esperados"

