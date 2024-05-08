import datetime
from typing import Union, Optional, Type

from starlette.responses import JSONResponse
from fastapi import status as fastapi_status
from pydantic import ValidationError

from core.models import (
    Todo,
    ApiResponse,
    User,
    TodoOut,
    ResponseStatus,
    TokenInfo,
)


def get_model_for_data(data: dict) -> Type[TokenInfo | User | Todo]:
    models = (TokenInfo, User, Todo)

    for model in models:
        try:
            if isinstance(data, list) and len(data) > 1:
                model.model_validate(data[0])
            else:
                model.model_validate(data)
            return model
        except ValidationError:
            pass


def prep_api_response(
        response_status: ResponseStatus,
        message: str,
        response_data: list[Todo] | TokenInfo | User | None,
        user: User | None,
        code: int = fastapi_status.HTTP_200_OK,
        cached: bool = False,
) -> JSONResponse:
    if response_data:
        response_data = eval(response_data) if cached else response_data
        model = get_model_for_data(response_data)
        if model in (TokenInfo, User):
            result = model.model_validate(response_data)
        else:
            result = [model.model_validate(element) for element in response_data]
            result = get_datetime_from_epoch(result)

    else:
        result = None
    actual_data = ApiResponse(
        status=response_status,
        code=code,
        message=message,
        data=result,
        cached=cached,
        user=user,
    )
    return JSONResponse(content=actual_data.model_dump())


def convert_epoch_to_datetime(todo: TodoOut) -> TodoOut:
    created_at_datetime = (
            datetime.datetime(1970, 1, 1)
            + datetime.timedelta(seconds=todo.created_at)
    )
    todo.created_at = str(created_at_datetime)
    return todo


def get_datetime_from_epoch(data:list[TodoOut]):
    return [convert_epoch_to_datetime(todo) for todo in data]
