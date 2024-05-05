"""Routers de la API"""

from fastapi import APIRouter

from .endpoints import aidtec, about

main_router = APIRouter()

main_router.include_router(aidtec.router, prefix='/aidtec', tags=['aidtec'])
main_router.include_router(about.router, prefix='/about', tags=['about'])