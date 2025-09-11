from fastapi import FastAPI
from uvicorn import run

from core.config import settings

app = FastAPI(title = settings.app_title)

if __name__ == "__main__":
    run(app="main:app", reload=True)
