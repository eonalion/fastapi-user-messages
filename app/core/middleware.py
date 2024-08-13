import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            f"Request: {request.method} {request.url.path} - Time: {process_time*1000:.0f} ms"
        )
        return response
