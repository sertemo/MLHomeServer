
import pytest

from mlhomeserver.exceptions import DataConfigError
from mlhomeserver.parser import DataParser

def test_data_parser_non_Existing_yml():
    with pytest.raises(DataConfigError):
        DataParser("aidtec", config_path="non_Existing.yml")


def test_data_parser_non_existing_competition():
    with pytest.raises(DataConfigError):
        DataParser("non_existing")


def test_loading_aidtec_correctly(aidtec_dataparser: DataParser):
    assert aidtec_dataparser.dataset_name == 'train.csv'
    assert aidtec_dataparser.label_col_name == 'calidad'


def test_get_preprocessor_module_correct(aidtec_dataparser: DataParser):
    returned = aidtec_dataparser._get_preprocessor_module()
    assert returned == 'mlhomeserver.ml.data_processing.aidtec_transformer'


def test_get_train_dataset_correct(aidtec_dataparser: DataParser):
    df = aidtec_dataparser.get_train_dataset()
    assert 'calidad' in df
    assert len(df) > 1
