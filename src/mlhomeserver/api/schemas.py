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

"""Módulo que recoge los esquemas de pydantic"""

from pydantic import BaseModel, Field
from typing import Any
from datetime import datetime


class Prediction(BaseModel):
    labels: list[int]
    length: int


class ModelInfo(BaseModel):
    last_trained: datetime
    parameters: dict[str, Any]
    competition: str

    def model_dump(self):
        # Convertir todos los datos del modelo a tipos serializables
        return {
            "last_trained": self.last_trained.isoformat(),
            "parameters": {k: str(v) for k, v in self.parameters.items()},
        }


class CustomResponse(BaseModel):
    status: str
    data: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)
    message: str
