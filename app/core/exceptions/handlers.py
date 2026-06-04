from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import StayEaseException


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(StayEaseException)
    async def stayease_exception_handler(
        request: Request,
        exc: StayEaseException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_response(exc.message),
            headers=exc.headers,
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        # Framework errors, such as missing bearer tokens, should match our API format.
        message = exc.detail if isinstance(exc.detail, str) else "Request failed"
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_response(message),
            headers=exc.headers,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        # Validation details can be added later; for now keep the public envelope simple.
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=_error_response("Validation failed"),
        )


def _error_response(message: str) -> dict[str, object | None]:
    return {
        "success": False,
        "message": message,
        "data": None,
    }
