from http import HTTPStatus
from typing import Any

from cherrytrack.types import FlaskResponse


def ok(**kwargs: Any) -> FlaskResponse:
    return {**kwargs}, HTTPStatus.OK
