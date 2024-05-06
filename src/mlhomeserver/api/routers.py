"""Agrupación de routers de la API en un main router"""

from fastapi import APIRouter

from .endpoints import about, model, predictions

main_router = APIRouter()

main_router.include_router(predictions.router, prefix="/predict", tags=["predict"])
main_router.include_router(model.router, prefix="/model", tags=["model"])
main_router.include_router(about.router, prefix="/about", tags=["about"])
