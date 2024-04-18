from config import settings
from core.pydantic_models import UserSchema, Role
from utils.constants import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from utils.security import encode_jwt


def create_jwt(
        token_type: str,
        token_payload: dict,
        expire_timedelta_sec: int | None = settings.AUTH_JWT.ACCESS_TOKEN_EXPIRE_SEC,
        expire_timedelta_days: int | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_payload)
    return encode_jwt(
        payload=jwt_payload,
        expire_timedelta_sec=expire_timedelta_sec,
        expire_timedelta_days=expire_timedelta_days,
    )


def create_access_token(user: UserSchema) -> str:
    jwt_payload = {
        "username": user.username,
        "email": user.email,
        "role": user.role.value if isinstance(user.role, Role) else user.role,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_payload=jwt_payload,
        expire_timedelta_sec=settings.AUTH_JWT.ACCESS_TOKEN_EXPIRE_SEC,
    )


def create_refresh_token(user: UserSchema) -> str:
    jwt_payload = {
        "sub": user.username,
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_payload=jwt_payload,
        expire_timedelta_days=settings.AUTH_JWT.REFRESH_TOKEN_EXPIRE_DAYS,
    )
