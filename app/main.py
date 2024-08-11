from fastapi import FastAPI

from app.api.routes import users, messages
from app.core.exception_handlers import setup_exception_handlers
from app.database import init_db

app = FastAPI()
setup_exception_handlers(app)

app.include_router(router=users.router, prefix="/users", tags=["users"])
app.include_router(
    router=messages.router, prefix="/users/{user_id}/messages", tags=["messages"]
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def read_root():
    return {"Hello": "World"}
