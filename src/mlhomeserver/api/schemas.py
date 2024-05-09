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