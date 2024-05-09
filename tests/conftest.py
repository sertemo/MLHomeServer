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

from pathlib import Path

from fastapi.testclient import TestClient
import pandas as pd
import pytest
from unittest.mock import patch

from mlhomeserver.main import app
from mlhomeserver.config import CONFIG_DICT
import mlhomeserver.settings as settings
from mlhomeserver.ml.training.trainer import Trainer
from mlhomeserver.parser import DataParser

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

# TODO Susceptible de cambiar
@pytest.fixture(scope="session")
def aidtec_competition_data():
    return CONFIG_DICT['aidtec']


@pytest.fixture(scope="session")
def train_aidtec_raw():
    # Cargamos el dataset
    df_train_raw = pd.read_csv(settings.DATA_PATH / "aidtec" / 'train.csv', index_col=0)
    return df_train_raw

@pytest.fixture(scope="session")
def train_aidtec_raw_no_label_col():
    # Cargamos el dataset
    df_train_raw = pd.read_csv(settings.DATA_PATH / "aidtec" / 'train.csv', index_col=0)
    return df_train_raw.drop(columns=['calidad'])

@pytest.fixture(scope="session")
def trainer_bad_preprocessor():
    trainer = Trainer(
        nombre_desafio="aidtec",
        label_col_name="calidad",
        train_dataset_filename="train.csv",
        train_dataset_index_col=0,
        preprocesador=object(),
        modelo=object(),
        label_encoder=True,
    )
    return trainer


@pytest.fixture(scope="session")
def aidtec_dataparser():
    return DataParser("aidtec")


@pytest.fixture(scope="session")
def trainer_bad_dataframe():
    trainer = Trainer(
        nombre_desafio="whatever",
        label_col_name="calidad",
        train_dataset_filename="train_que_no_existe.csv",
        preprocesador=object(),
        modelo=object(),
        label_encoder=True,
    )
    return trainer

@pytest.fixture(scope="session")
def trainer_bad_label_col_namee():
    trainer = Trainer(
        nombre_desafio="aidtec",
        label_col_name="calidad",
        train_dataset_filename="train.csv",
        preprocesador=object(),
        modelo=object(),
        label_encoder=True,
    )
    return trainer

@pytest.fixture
def mock_trainer():  # Patchearlo donde SE USA, NO donde se define
    with patch('mlhomeserver.ml.training.train.Trainer') as TrainerMock:
        yield TrainerMock