from urllib.request import Request
from starlette.responses import JSONResponse

from app.core.exceptions import NotFoundError, AlreadyExistsError


def not_found_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={"message": str(exc)}
    )


def bad_request_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )


def setup_exception_handlers(app):
    app.add_exception_handler(NotFoundError, not_found_exception_handler)
    app.add_exception_handler(AlreadyExistsError, bad_request_exception_handler)
