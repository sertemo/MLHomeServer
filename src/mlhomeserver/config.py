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

"""Módulo con las diferentes configuraciones de cada desafío"""


from sklearn.ensemble import RandomForestClassifier

from mlhomeserver.ml.data_processing.aidtec_transformer import WineDatasetTransformer

CONFIG_DICT = {
    "aidtec": {
        "train_dataset_filename": "train.csv",  # En data/aidtec
        "label_col_name": "calidad",
        "preprocesador": WineDatasetTransformer(
            drop_columns=[
                "year",
                "color",
                "alcohol",
                "densidad",
                "dioxido de azufre libre",
            ]
        ),
        "modelo": RandomForestClassifier(n_estimators=900, random_state=42),
        "label_encoder": True,
    },
}
