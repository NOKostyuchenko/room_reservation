from fastapi import FastAPI
from uvicorn import run
from api.routers import main_router
from core.config import settings

app = FastAPI(title=settings.app_title, docs_url="/swagger")

app.include_router(main_router)

if __name__ == "__main__":
    run(app="main:app")
