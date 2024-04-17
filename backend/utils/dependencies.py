from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis

from core.models import User, TokenInfo
from core.services import AuthUserService, TodoService, get_todo_service
from utils.cache import init_redis_pool

# redis cache dependency
redis_dependency = Annotated[Redis, Depends(init_redis_pool)]

get_user_by_token_dependency = Annotated[User, Depends(AuthUserService.check_access_token)]

get_todo_service_dependency = Annotated[TodoService, Depends(get_todo_service)]

refresh_tokens_dependency = Annotated[TokenInfo, Depends(AuthUserService.refresh_tokens)]
