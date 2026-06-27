from fastapi import FastAPI
from .db.database import engine, Base
from .routers import auth
#from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/greeting")
def greeting():
    return{"Hello"}

app.include_router(auth.router)
