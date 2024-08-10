from fastapi import FastAPI

from app.api.routes import users
from app.database import init_db

app = FastAPI()

app.include_router(router=users.router, prefix="/users", tags=["users"])


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.on_event("startup")
def on_startup():
    init_db()
