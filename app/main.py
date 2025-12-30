from fastapi import FastAPI
from uvicorn import run
from fastapi.middleware.cors import CORSMiddleware

from api.routers import main_router
from core.configs import app_settings

app = FastAPI(title=app_settings.app_title, docs_url="/swagger")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

app.include_router(main_router)

if __name__ == "__main__":
    run(
        app="main:app",
        host=app_settings.app_host,
        port=app_settings.app_port
    )
