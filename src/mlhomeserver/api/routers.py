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

"""Agrupación de routers de la API en un main router"""

from fastapi import APIRouter

from .endpoints import about, model, predictions

main_router = APIRouter()

main_router.include_router(predictions.router, prefix="/predict", tags=["predict"])
main_router.include_router(model.router, prefix="/model", tags=["model"])
main_router.include_router(about.router, prefix="/about", tags=["about"])
