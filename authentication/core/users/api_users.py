from __future__ import annotations

# from app.utils.response_utils import user_response
from fastapi import APIRouter, Response, status

from core.pydantic_models import UserSchema, UserSchemaCreate, UserSchemaUpdate
from core.users.services import UsersService
from utils.dependencies import uow_dependency

router = APIRouter(prefix="/users", tags=["utils"])


# @router.get("/me", response_model=UserSchema)
# async def get_current_user_route(
#     current_user: current_user_dependency,
# ) -> UserSchema:
#     """endpoint for getting current user"""
#     return user_response(current_user)


@router.get("/{user_id}", response_model=UserSchema)
async def read_user_by_id_route(
        user_id: int,
        uow: uow_dependency,
) -> UserSchema:
    """endpoint for reading one user data by user_id"""
    return await UsersService.get(uow, user_id)


@router.get("/", response_model=list[UserSchema])
async def read_all_users_route(
        uow: uow_dependency,
) -> list[UserSchema]:
    """endpoint for reading all users"""
    return await UsersService.get_list(uow)


@router.post("/", response_model=UserSchema)
async def crate_user_route(
        user_data: UserSchemaCreate,
        uow: uow_dependency,
) -> UserSchema:
    """endpoint for creating new user"""
    return await UsersService.create(uow, user_data)


@router.delete("/{user_id}")
async def delete_user_route(
        user_id: int,
        uow: uow_dependency,
) -> Response:
    """endpoint for deleting particular user data by user id"""
    await UsersService.delete(uow, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{user_id}", response_model=UserSchema)
async def update_user_route(
        user_id: int,
        user_data: UserSchemaUpdate,
        uow: uow_dependency,
) -> UserSchema:
    """endpoint for creating new user"""
    return await UsersService.update(uow, user_id, user_data)
