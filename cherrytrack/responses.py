from http import HTTPStatus
from typing import Any, Union, List

from cherrytrack.types import FlaskResponse


def ok(**kwargs: Any) -> FlaskResponse:
    return {**kwargs}, HTTPStatus.OK


def internal_server_error(errors: Union[str, List[str]], **kwargs: Any) -> FlaskResponse:
    if isinstance(errors, str):
        return {"errors": [errors], **kwargs}, HTTPStatus.INTERNAL_SERVER_ERROR

    return {"errors": errors, **kwargs}, HTTPStatus.INTERNAL_SERVER_ERROR
