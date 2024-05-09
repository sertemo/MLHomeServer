from pathlib import Path
from unittest.mock import patch

import pytest
from sklearn.ensemble import RandomForestClassifier

from mlhomeserver.exceptions import (
    DataConfigError,
    PreProcessorModuleLoadError,
    NonValidPreProcessor,
    ModelModuleLoadError,
    NonValidModel,
    NotFoundTrainDFError,
    NonValidDataset
)
from mlhomeserver.parser import DataParser


def test_get_dataset_aidtec_wrong_dataset_path():
    dp = DataParser('aidtec')
    with patch.object(dp, '_get_train_dataset_path', return_value=Path('No_valido')):
        with pytest.raises(NotFoundTrainDFError):
            dp.get_train_dataset()


def test_data_parser_non_existing_yml():
    with pytest.raises(DataConfigError):
        DataParser("aidtec", config_path="non_existing.yml")


def test_data_parser_non_existing_competition():
    with pytest.raises(DataConfigError):
        DataParser("non_existing")


def test_loading_aidtec_correctly(aidtec_dataparser: DataParser):
    assert aidtec_dataparser.dataset_name == 'train.csv'
    assert aidtec_dataparser.label_col_name == 'calidad'


def test_get_preprocessor_module_correct(aidtec_dataparser: DataParser):
    returned = aidtec_dataparser._get_preprocessor_module()
    assert returned == 'mlhomeserver.ml.data_processing.aidtec_transformer'


def test_get_model_module_correct(aidtec_dataparser: DataParser):
    returned = aidtec_dataparser._get_model_module()
    assert returned == 'sklearn.ensemble'


def test_loading_preprocessor_wrong_module():
    dp = DataParser('aidtec')
    with patch.object(dp, '_get_preprocessor_module', return_value='wrong.module.name'):
        with pytest.raises(PreProcessorModuleLoadError):
            dp.get_preprocessor()


def test_loading_preprocessor_correct_aidtec():
        dp = DataParser('aidtec')
        preprocessor = dp.get_preprocessor()
        assert preprocessor.__class__.__name__ == "WineDatasetTransformer"


def test_loading_model_wrong_module():
    dp = DataParser('aidtec')
    with patch.object(dp, '_get_model_module', return_value='wrong.module.name'):
        with pytest.raises(ModelModuleLoadError):
            dp.get_model()


def test_get_preprocessor_params_aidtec_correct(aidtec_dataparser: DataParser):
    assert aidtec_dataparser.get_preprocessor_params() == {
        "drop_columns": [
            "year",
            "color",
            "alcohol",
            "densidad",
            "dioxido de azufre libre"
        ]
    }


def test_get_preprocessor_non_valid():
    dp = DataParser('aidtec')
    with patch.object(dp, '_load_preprocessor', return_value=object()):
        with pytest.raises(NonValidPreProcessor):
            dp.get_preprocessor()


def test_get_model_params_aidtec_correct(aidtec_dataparser: DataParser):
    assert aidtec_dataparser.get_model_params() == {
        'n_estimators': 900,
        'random_state': 42
    }


def test_get_model_non_valid_model():
    dp = DataParser('aidtec')  # TODO Mocking
    with patch.object(dp, '_load_model', return_value=object()):
        with pytest.raises(NonValidModel):
            dp.get_model()


def test_validate_preprocessor_non_valid_preprocessor(aidtec_dataparser: DataParser):
    with pytest.raises(NonValidPreProcessor):
        aidtec_dataparser._validate_preprocessor(object)


def test_get_model_aidtec_correct(aidtec_dataparser: DataParser):
    modelo: RandomForestClassifier = aidtec_dataparser.get_model()
    assert isinstance(modelo, RandomForestClassifier)
    assert modelo.n_estimators == 900
    assert modelo.random_state == 42


def test_get_label_encoder_aidtec_correct(aidtec_dataparser: DataParser):
    assert aidtec_dataparser.get_label_encoder() == True


def test_get_train_dataset_correct(aidtec_dataparser: DataParser):
    df = aidtec_dataparser.get_train_dataset()
    assert 'calidad' in df
    assert len(df) > 1

    if 'index_col' in aidtec_dataparser.get_dataset_params():
        # Si hemos pasado índice en el yml, la primera columna no puede
        # ser muestra_id
        assert df.columns[0] != 'muestra_id' 
