from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        from_attributes = True


class Role(Enum):
    admin = "admin"
    user = "user"
    god = "god"


# ====================== user's models ==========================
class UserBase(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    role: Role = "user"


class UserSchema(UserBase, TunedModel):
    id: int

    class Config:
        arbitrary_types_allowed = True


class UserSchemaCreate(UserBase):
    password: str


class UserSchemaUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    email: EmailStr | None = None


# ====================== token's models ==========================
class Token(BaseModel):
    access_token: str
    token_type: str
