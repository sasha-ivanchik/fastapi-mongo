from dataclasses import dataclass
from enum import Enum
from typing import Union, Any
from datetime import datetime

from pydantic import BaseModel, model_validator
from fastapi import status

from utils.exceptions import SuperApiException


class TodoBase(BaseModel):
    title: str
    description: str
    additional_info: dict[
                         str,
                         Union[str, int, float]
                     ] | str | None = None
    is_done: bool = False
    public: bool = True


class TodoCreate(TodoBase):
    ...

    @model_validator(mode="before")
    @classmethod
    def check_if_title_and_desc_exist(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get("title"):
                raise SuperApiException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail="A `title` must be provided.",
                )
            if not data.get("description") and not (data.get("additional_info")):
                raise SuperApiException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail="A `description` must be provided.",
                )
        return data


class TodoUpdate(BaseModel):
    description: str | None = None
    additional_info: dict[
                         str,
                         Union[str, int, float]
                     ] | str | None = None
    public: bool | None = None
    is_done: bool | None = None


class TodoOut(TodoBase):
    created_at: float | datetime


class Todo(TodoOut):
    username: str


class User(BaseModel):
    username: str
    email: str
    role: str


# ===================== comon response ==========================

class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


@dataclass
class ResponseStatus(str, Enum):
    success = "success"
    error = "error"


class ApiResponse(BaseModel):
    status: ResponseStatus | str
    message: str
    data: TokenInfo | list[TodoOut] | User | None
    code: int = 200
    cached: bool = False
    user: User | None

    class Config:
        from_attributes = True
