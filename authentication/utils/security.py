import datetime
from datetime import timedelta
from typing import Union

import jwt

from config import settings


def encode_jwt(
        payload: dict,
        private_key: str = settings.AUTH_JWT.PRIVATE_KEY_PATH.read_text(),
        algorithm: str = settings.AUTH_JWT.ALGORITHM,
        expire_timedelta_sec: int = settings.AUTH_JWT.ACCESS_TOKEN_EXPIRE_SEC,
):
    to_encode = payload.copy()
    expire = datetime.datetime.utcnow() + timedelta(seconds=expire_timedelta_sec)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        private_key,
        algorithm,
    )
    return encoded_jwt


def decode_jwt(
        encoded_token: Union[str, bytes],
        public_key: str = settings.AUTH_JWT.PUBLIC_KEY_PATH.read_text(),
        algorithm: str = settings.AUTH_JWT.ALGORITHM,
):
    encoded_jwt = jwt.decode(
        encoded_token,
        public_key,
        algorithms=[algorithm],
    )
    return encoded_jwt
