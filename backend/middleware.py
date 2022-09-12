import logging
from contextvars import ContextVar
from uuid import uuid4

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request

from backend.dtos.common import InternalServerErrorResponse
from backend.settings import Settings

settings = Settings()
logger = logging.getLogger(__name__)

REQUEST_ID_CTX_KEY = "request_id"

_request_id_ctx_var: ContextVar[str] = ContextVar(REQUEST_ID_CTX_KEY, default=None)


def get_request_id() -> str:
    return _request_id_ctx_var.get()


class RequestContextLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        request_id = _request_id_ctx_var.set(str(uuid4()))
        logger.info(f"{request.method} {request.url}")
        logger.debug(f"Headers: {request.headers.items()}")

        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = get_request_id()
        except Exception as exc:
            logger.error(exc.__repr__(), exc_info=1)
            return JSONResponse(
                headers={"X-Request-ID": get_request_id()},
                status_code=500,
                content=InternalServerErrorResponse(
                    detail=str(exc.__repr__()), url=str(request.url)
                ).dict(),
            )

        _request_id_ctx_var.reset(request_id)

        return response
