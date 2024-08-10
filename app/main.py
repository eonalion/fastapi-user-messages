from fastapi import FastAPI

from app.api.routes import users, messages
from app.database import init_db

app = FastAPI()

app.include_router(router=users.router, prefix="/users", tags=["users"])
app.include_router(router=messages.router, prefix="/users/{user_id}/messages", tags=["messages"])


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def read_root():
    return {"Hello": "World"}
