from core.models import Todo, ApiResponse, User, TodoBase


def prep_api_response(
        response_data: Todo | list[Todo] | None,
        user: User,
        cached: bool = False,
) -> ApiResponse:
    result = (
        TodoBase.model_validate(response_data)
        if not isinstance(response_data, list)
        else [TodoBase.model_validate(element) for element in response_data]
    )
    return ApiResponse(result=result, cached=cached, user=user)
