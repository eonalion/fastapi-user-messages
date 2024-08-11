from urllib.request import Request

from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from app.core.exceptions import NotFoundError, AlreadyExistsError


def not_found_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": str(exc)})


def conflict_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=409, content={"message": str(exc)})


def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    formatted_errors = []
    for error in exc.errors():
        location = " -> ".join(str(loc) for loc in error["loc"])
        error_message = f"{location}: {error['msg']}"
        formatted_errors.append(error_message)

    return JSONResponse(
        status_code=400,
        content={"detail": formatted_errors},
    )


def setup_exception_handlers(app):
    app.add_exception_handler(NotFoundError, not_found_exception_handler)
    app.add_exception_handler(AlreadyExistsError, conflict_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
