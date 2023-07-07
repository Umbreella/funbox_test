from fastapi import status
from fastapi.responses import JSONResponse


class GeneralJsonResponse(JSONResponse):
    def __init__(
        self, status_msg: str, status_code: status, data: dict = None,
    ):
        content = {
            'status': status_msg,
        }

        if data:
            content.update(**data)

        super().__init__(content, status_code)
