from fastapi import FastAPI

from app.core.exception_handlers import setup_exception_handlers
from app.core.middleware import LoggingMiddleware
from app.database import init_db
from app.api.routes.api import router as api_router


app = FastAPI()
setup_exception_handlers(app)
app.add_middleware(LoggingMiddleware)
app.include_router(api_router)


@app.on_event("startup")
def on_startup():
    init_db()
