from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Any, Optional


class RsBaseResponse(JSONResponse):

    def __init__(
            self,
            content: Any,
            status_code: int = 200,
            headers: Optional[dict[str, str]] = None,
    ) -> None:
        super().__init__(content, status_code, headers)


class RsResponse(RsBaseResponse):
    @staticmethod
    def resp_200(data: Any) -> JSONResponse:
        """
        Return a 200 OK response with the provided data.
        """
        response_data = {
            'code': 0,
            'message': "Success",
            'data': data,
        }
        return RsBaseResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(response_data, exclude_none=False)
        )

    @staticmethod
    def resp_400(data: Any, message: str = 'Bad Request!') -> JSONResponse:
        """
        Return a 400 Bad Request response with the provided data and message.
        """
        response_data = {
            'code': 1,
            'message': message,
            'data': data,
        }
        return RsBaseResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(response_data, exclude_none=True)
        )

    @staticmethod
    def resp_500(data: Any, message: str = 'Internal Server Error!') -> JSONResponse:
        """
        Return a 500 Internal Server Error response with the provided data and message.
        """
        response_data = {
            'code': 1,
            'message': message,
            'data': data,
        }
        return RsBaseResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(response_data, exclude_none=True)
        )

    @staticmethod
    def resp_501(data: Any) -> JSONResponse:
        """
        Return a 501 Not Implemented response with the provided data.
        """
        response_data = {
            'code': 0,
            'message': "Success",
            'data': data,
        }
        return RsBaseResponse(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            content=jsonable_encoder(response_data, exclude_none=False)
        )
