"""Entry point principal de la app"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from mlhomeserver.api.routers import main_router

app = FastAPI()

app.include_router(main_router)


@app.get("/")
async def root():
    return JSONResponse(content={"ML Home Server": "by STM"})


if __name__ == "__main__":
    pass
