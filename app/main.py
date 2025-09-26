from fastapi import FastAPI
from uvicorn import run
from api.meeting_room import router
from core.config import settings

app = FastAPI(title=settings.app_title, docs_url="/swagger")

app.include_router(router)

if __name__ == "__main__":
    run(app="main:app")
