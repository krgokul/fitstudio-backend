from fastapi import HTTPException, status


class RecordNotFound(HTTPException):
    def __init__(self, msg) -> None:
        status_code = status.HTTP_404_NOT_FOUND
        detail = msg
        super().__init__(status_code, detail)


class RecordExists(HTTPException):
    def __init__(self, msg) -> None:
        status_code = status.HTTP_400_BAD_REQUEST
        detail = msg
        super().__init__(status_code, detail)


class BadRequestException(HTTPException):
    def __init__(self, msg) -> None:
        status_code = status.HTTP_400_BAD_REQUEST
        detail = msg
        super().__init__(status_code, detail)
