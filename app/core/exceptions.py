from fastapi import status


class StayEaseException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.headers = headers
