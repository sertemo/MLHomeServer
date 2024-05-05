"""Entry point principal de la app"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .api.routers import main_router

app = FastAPI()

app.include_router(main_router)

@app.get('/')
async def root():
    return JSONResponse(content={'info': 'API en pruebas para lanzar predicciones'})

if __name__ == '__main__':
    pass