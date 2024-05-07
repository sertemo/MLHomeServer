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

from mlhomeserver.main import app
import mlhomeserver.settings as settings
from mlhomeserver.ml.training.trainer import Trainer

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(scope="session")
def trainer_bad_preprocessor():
    trainer = Trainer(
        nombre_desafio="whatever",
        label_col_name="calidad",
        train_dataset=pd.read_csv(
            settings.DATA_PATH / "aidtec" / "train.csv", index_col=0
        ),
        preprocesador=object(),
        modelo=object(),
        label_encoder=True,
    )
    return trainer

@pytest.fixture(scope="session")
def trainer_bad_dataframe():
    trainer = Trainer(
        nombre_desafio="whatever",
        label_col_name="calidad",
        train_dataset=pd.DataFrame(),
        preprocesador=object(),
        modelo=object(),
        label_encoder=True,
    )
    return trainer