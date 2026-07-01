from fastapi import FastAPI
from .db.database import engine, Base
from .routers import auth, interview, interview_result, history

from fastapi.staticfiles import StaticFiles
from pathlib import Path

#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/audio",
    StaticFiles(directory=BASE_DIR / "audio"),
    name="audio"
)

app.include_router(auth.router)
app.include_router(interview.router)
app.include_router(interview_result.router)
app.include_router(history.router)