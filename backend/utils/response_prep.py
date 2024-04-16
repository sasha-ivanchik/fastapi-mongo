import json
import datetime

from core.models import Todo, ApiResponse, User, TodoBase


def prep_api_response(
        response_data: Todo | list[Todo] | str,
        user: User,
        cached: bool = False,
) -> ApiResponse:
    response_data = eval(response_data) if cached else response_data
    result = (
        Todo.model_validate(response_data)
        if not isinstance(response_data, list)
        else [Todo.model_validate(element) for element in response_data]
    )
    result = get_datetime_from_epoch(result)
    return ApiResponse(result=result, cached=cached, user=user)


def convert_epoch_to_datetime(todo: Todo) -> Todo:
    created_at_datetime = (
            datetime.datetime(1970, 1, 1)
            + datetime.timedelta(seconds=todo.created_at)
    )
    todo.created_at = created_at_datetime
    return todo


def get_datetime_from_epoch(data: Todo | list[Todo]):
    if isinstance(data, Todo):
        return convert_epoch_to_datetime(data)
    else:
        return [convert_epoch_to_datetime(todo) for todo in data]
