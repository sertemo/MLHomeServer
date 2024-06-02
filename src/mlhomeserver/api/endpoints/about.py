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

"""Módulo del endpoint about"""

import platform

from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from mlhomeserver.utils import get_project_version

router = APIRouter(responses={404: {"mensaje": "No encontrado"}}, tags=["about"])


@router.get("/")
async def about():
    return JSONResponse(
        content={
            "status": "OK",
            "project": {
                "nombre": "ML Home Server",
                "version": get_project_version(),
                "descripción": (
                    "API para lanzar predicciones de modelos "
                    "de ML previamente entrenados y que corresponden con los desafíos "
                    "de la web de Kopuru."
                ),
            },
            "autor": {
                "nombre": "Sergio Tejedor",
                "web": "https://tejedormoreno.com",
                "github": "https://github.com/sertemo",
                "Linkdin": "www.linkedin.com/in/sertemo",
            },
            "server": {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
            },
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }
    )
