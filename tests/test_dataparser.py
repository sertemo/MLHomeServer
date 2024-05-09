from unittest.mock import patch

import pytest

from mlhomeserver.exceptions import DataConfigError, PreProcessorModuleLoadError, NonValidPreProcessor
from mlhomeserver.parser import DataParser

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


def test_loading_preprocessor_wrong_module():
    dp = DataParser('aidtec')
    dp._get_preprocessor_module = lambda : 'wrong.module.name'
    with pytest.raises(PreProcessorModuleLoadError):
        dp.get_preprocessor()


def test_loading_preprocessor_correct_aidtec():
        dp = DataParser('aidtec')
        preprocessor = dp.get_preprocessor()
        assert preprocessor.__class__.__name__ == "WineDatasetTransformer"


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


def test_validate_preprocessor_non_valid_preprocessor(aidtec_dataparser: DataParser):
    with pytest.raises(NonValidPreProcessor):
        aidtec_dataparser._validate_preprocessor(object)


def test_get_train_dataset_correct(aidtec_dataparser: DataParser):
    df = aidtec_dataparser.get_train_dataset()
    assert 'calidad' in df
    assert len(df) > 1

    if 'index_col' in aidtec_dataparser.get_dataset_params():
        # Si hemos pasado índice en el yml, la primera columna no puede
        # ser muestra_id
        assert df.columns[0] != 'muestra_id' 
