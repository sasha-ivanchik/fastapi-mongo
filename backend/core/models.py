from typing import Union, Any

from pydantic import BaseModel, model_validator
from fastapi import status

from utils.exceptions import SuperApiException


class TodoBase(BaseModel):
    title: str
    description: str
    additional_info: dict | str | None = None


class TodoCreate(TodoBase):
    ...


class TodoUpdate(TodoBase):
    description: str | None
    additional_info: dict | str | None = None

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
                    detail="A `description` or `additional_info` must be provided.",
                )
        return data


class Todo(TodoBase):
    username: str


class User(BaseModel):
    username: str
    email: str
    role: str


class ApiResponse(BaseModel):
    result: Union[list[TodoBase], TodoBase]
    cached: bool = False
    user: User


class Token(BaseModel):
    access_token: str
    token_type: str
