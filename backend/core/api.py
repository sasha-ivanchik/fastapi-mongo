import json

from fastapi import APIRouter, status, Form, Request

from utils.celery_worker import celery_set_cache, celery_delete_cached_key
from config import settings as global_settings
from core.models import (
    ApiResponse,
    TodoCreate,
    TodoUpdate,
    ResponseStatus,
)
from core.services import AuthUserService
from utils.dependencies import (
    redis_dependency,
    get_user_by_token_dependency,
    get_todo_service_dependency,
    refresh_tokens_dependency,
)
from utils.response_prep import (
    prep_api_response,
)

router = APIRouter(prefix="/api")

collection = global_settings.mongo_collection


@router.get("/")
def health() -> dict:
    return {"ping": "pong"}


@router.post("/todo", response_model=ApiResponse)
async def create_todo(
        user: get_user_by_token_dependency,
        todo_service: get_todo_service_dependency,
        todo: TodoCreate,
):
    # insert data
    new_todo = await todo_service.create_document(user, todo)

    # remove cache for particular user
    celery_delete_cached_key.delay(
        cache_key=f"{user.username}_todos",
    )
    return prep_api_response(
        response_status=ResponseStatus.success.value,
        message="New TODO has been successfully created.",
        response_data=new_todo,
        user=user,
    )


@router.get("/todo", response_model=ApiResponse)
async def get_all_todos(
        user: get_user_by_token_dependency,
        todo_service: get_todo_service_dependency,
        redis_client: redis_dependency,
):
    user_todos = f"{user.username}_todos"
    all_todos_message = "All your TODOs."

    # check cache
    if (cached_todos := await redis_client.get(user_todos)) is not None:
        cached_todos = json.loads(cached_todos)
        return prep_api_response(
            response_status=ResponseStatus.success.value,
            message=all_todos_message,
            response_data=cached_todos,
            user=user,
            cached=True,
        )

    # if no cache
    todos = await todo_service.retrieve_all_documents(user=user)

    celery_set_cache.delay(
        cache_key=user_todos,
        payload=json.dumps(str(todos)),
        expire=global_settings.cache_time_sec,
    )
    return prep_api_response(
        response_status=ResponseStatus.success.value,
        message=all_todos_message,
        response_data=todos,
        user=user,
    )


@router.get("/todo/{title}", response_model=ApiResponse)
async def get_todo_by_title(
        title: str,
        user: get_user_by_token_dependency,
        todo_service: get_todo_service_dependency,
        redis_client: redis_dependency,
):
    todo_key = f"{user.username}_{title}"
    todo_by_name_message = "TODO found by title."

    # check cache
    if (cached_todo := await redis_client.get(todo_key)) is not None:
        cached_todo = json.loads(cached_todo)
        return prep_api_response(
            response_status=ResponseStatus.success.value,
            message=todo_by_name_message,
            response_data=cached_todo,
            user=user,
            cached=True,
        )

    # if no cache
    todo = await todo_service.retrieve_document(
        user=user,
        title=title,
    )

    celery_set_cache.delay(
        cache_key=todo_key,
        payload=json.dumps(str([todo])),
        expire=global_settings.cache_time_sec,
    )

    return prep_api_response(
        response_status=ResponseStatus.success.value,
        message=todo_by_name_message,
        response_data=todo,
        user=user,
    )


@router.put("/todo/{title}", response_model=ApiResponse)
@router.patch("/todo/{title}", response_model=ApiResponse)
async def update_todo_by_id(
        title: str,
        update_todo: TodoUpdate,
        todo_service: get_todo_service_dependency,
        user: get_user_by_token_dependency,
):
    response = await todo_service.update_document(
        user=user,
        title=title,
        update_todo=update_todo,
    )

    # clear cache for user in background
    celery_delete_cached_key.delay(
        cache_key=f"{user.username}_todos",
    )
    celery_delete_cached_key.delay(
        cache_key=f"{user.username}_{title}",
    )
    return prep_api_response(
        response_status=ResponseStatus.success.value,
        message="TODO updated successfully.",
        response_data=response,
        user=user,
    )


@router.delete("/todo/{title}", response_model=ApiResponse)
async def delete_todo_by_id(
        title: str,
        todo_service: get_todo_service_dependency,
        user: get_user_by_token_dependency,
):
    await todo_service.delete_document(user=user, title=title)

    celery_delete_cached_key.delay(
        cache_key=f"{user.username}_todos",
    )
    celery_delete_cached_key.delay(
        cache_key=f"{user.username}_{title}",
    )
    return prep_api_response(
        code=status.HTTP_204_NO_CONTENT,
        response_status=ResponseStatus.success.value,
        message="TODO deleted successfully.",
        response_data=None,
        user=user,
    )


@router.post("/login", response_model=ApiResponse, tags=["auth"])
async def proxy_to_login(
        request: Request,
        username: str = Form(),
        password: str = Form(),
):
    response_data = await AuthUserService.login_user(
        username=username,
        password=password,
        request=request,
    )
    return prep_api_response(
        response_status=ResponseStatus.success.value,
        message="Client has successfully logged in.",
        response_data=response_data,
        user=None,
    )


@router.post("/signup", response_model=ApiResponse, tags=["auth"])
async def proxy_to_signup(
        request: Request,
        email: str = Form(),
        password: str = Form(),
        username: str = Form(),
):
    response_data = await AuthUserService.signup_user(
        username=username,
        password=password,
        email=email,
        request=request,
    )
    return prep_api_response(
        response_status=ResponseStatus.success.value,
        message="Client has been successfully registered.",
        response_data=response_data,
        user=None,
    )


@router.get("/check", response_model=ApiResponse, tags=["auth"])
async def proxy_to_check(
        user: get_user_by_token_dependency,
):
    return prep_api_response(
        response_status=ResponseStatus.success.value,
        message="Client information provided.",
        response_data=user,
        user=None,
    )


@router.get("/refresh", tags=["auth"])
async def proxy_to_refresh(
        token_info: refresh_tokens_dependency,
):
    return prep_api_response(
        response_status=ResponseStatus.success.value,
        message="Access data has been successfully updated.",
        response_data=token_info,
        user=None,
    )
