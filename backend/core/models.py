from typing import Union, Any
from datetime import datetime, timezone

from pydantic import BaseModel, model_validator
from fastapi import status

from utils.exceptions import SuperApiException


class TodoBase(BaseModel):
    title: str
    description: str
    additional_info: dict | str | None = None
    is_done: bool = False
    public: bool = True


class TodoCreate(TodoBase):
    ...


class TodoUpdate(TodoBase):
    description: str | None
    additional_info: dict | str | None = None
    public: bool | None = None
    is_done: bool | None = None

    @model_validator(mode="before")
    @classmethod
    def check_card_number_omitted(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get("title"):
                raise SuperApiException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail="A `title` must be provided.",
                )
            if not data.get("description") and not (data.get("additional_info")):
                raise SuperApiException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    # detail="`description` or `additional_info` must be provided.",
                    detail="A `description` must be provided.",
                )
        return data


class Todo(TodoBase):
    created_at: float | datetime


class User(BaseModel):
    username: str
    email: str
    role: str


class ApiResponse(BaseModel):
    result: Union[list[Todo], Todo]
    cached: bool = False
    user: User


class Token(BaseModel):
    access_token: str
    token_type: str
