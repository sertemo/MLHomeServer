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


from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


class EfficiencyTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.efficiency_preprocessor = Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                (
                    "rfe",
                    RFE(
                        estimator=RandomForestClassifier(random_state=42),
                        n_features_to_select=5,
                    ),
                ),
            ]
        )

    def fit(self, X, y=None):
        print("fit")
        self.efficiency_preprocessor.fit(X, y)
        return self

    def transform(self, X):
        print("transform")
        return self.efficiency_preprocessor.transform(X)
