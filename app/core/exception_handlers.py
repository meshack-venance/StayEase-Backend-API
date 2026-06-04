from fastapi import FastAPI, Request
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
            content={
                "success": False,
                "message": exc.message,
            },
            headers=exc.headers,
        )
