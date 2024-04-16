from typing import Annotated, AsyncGenerator

from fastapi import Depends

from core.connection import get_session
from core.schemas import User
from utils.helpers import (
    get_user_by_credentials,
    get_user_by_access_token,
    get_user_by_refresh_token,
)
from utils.unit_of_work import ProtocolUnitOfWork, UnitOfWork

uow_dependency = Annotated[ProtocolUnitOfWork, Depends(UnitOfWork)]

user_by_credentials_dependency = Annotated[User, Depends(get_user_by_credentials)]

user_by_token_dependency = Annotated[User, Depends(get_user_by_access_token)]
user_by_refresh_token_dependency = Annotated[User, Depends(get_user_by_refresh_token)]

session_dependency = Annotated[AsyncGenerator, Depends(get_session)]
