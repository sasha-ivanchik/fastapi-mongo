import time

from fastapi import status, Request, Header
import httpx

from utils.exceptions import SuperApiException
from .models import (
    Todo,
    TodoCreate,
    TokenInfo,
    User,
    TodoUpdate, ResponseStatus,
)
from config import settings
from .repository import Repository, MongoRepository


class TodoService:
    repository = None

    def __init__(self):
        self.repository: Repository = MongoRepository()

    async def retrieve_all_documents(
            self,
            user: User,
    ) -> list[Todo]:
        """returns all documents by username field"""

        document_filter = {"username": user.username}
        db_query = await self.repository.get_list(document_filter)

        todos = (
            [document async for document in db_query]
            if db_query
            else []
        )
        return todos

    async def retrieve_document(
            self,
            user: User,
            title: str,
    ) -> Todo:
        """returns unique document by username and title fields"""

        document_filter = {"title": title, "username": user.username}

        if document := await self.repository.get(document_filter):
            return Todo.model_validate(document)
        else:
            raise SuperApiException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No data",
            )

    async def create_document(
            self,
            user: User,
            incoming_todo: TodoCreate,
    ) -> Todo:
        """creates new todo_document in DB and returns it"""

        try:
            if await self.repository.get(
                    {"title": incoming_todo.title, "username": user.username}
            ):
                raise SuperApiException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Already exist",
                )

            new_todo = Todo(
                created_at=time.time(),
                username=user.username,
                title=incoming_todo.title,
                description=incoming_todo.description,
                additional_info=incoming_todo.additional_info,
                is_done=incoming_todo.is_done,
                public=incoming_todo.public,
            )
            new_todo_in_db = await self.repository.create(new_todo.model_dump())

            return Todo.model_validate(new_todo_in_db)

        except SuperApiException:
            raise

        except Exception as e:
            raise SuperApiException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                # detail="Something went wrong. Retry.",
                detail=str(e),
            )

    async def update_document(
            self,
            user: User,
            title: str,
            update_todo: TodoUpdate,
    ) -> Todo:
        """updates todo_document in DB and returns it"""

        doc_filter = {"title": title, "username": user.username}
        doc_setter = update_todo.model_dump(exclude_none=True)

        document = await self.repository.update(doc_filter, doc_setter)
        if document:
            return Todo.model_validate(document)

        raise SuperApiException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong. Retry.",
        )

    async def delete_document(
            self,
            user: User,
            title: str,
    ) -> bool:
        """deletes todo_document from DB"""

        doc_filter = {"title": title, "username": user.username}
        await self.repository.delete(doc_filter)
        return True


async def get_todo_service():
    return TodoService()


class AuthUserService:
    @staticmethod
    async def login_user(
            username: str,
            password: str,
            request: Request,
    ) -> TokenInfo:
        data = {
            "username": username,
            "password": password,
        }

        headers = request.headers.mutablecopy()
        del headers["Content-Length"]
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.LOGIN_URL,
                headers=headers,
                data=data,
            )
            response = response.json()
        if response.get("status") != ResponseStatus.success:
            raise SuperApiException(
                status_code=int(response.get('code')),
                detail=response.get('message'),
            )
        return response.get("data")

    @staticmethod
    async def signup_user(
            request: Request,
            email: str,
            password: str,
            username: str,
    ) -> TokenInfo:
        data = {
            "username": username,
            "password": password,
            "email": email,
        }

        headers = request.headers.mutablecopy()
        del headers["Content-Length"]
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.SIGNUP_URL,
                headers=headers,
                data=data,
            )
            response = response.json()
            if response.get("status") != ResponseStatus.success:
                raise SuperApiException(
                    status_code=int(response.get('code')),
                    detail=response.get('message'),
                )
        return response.get('data')

    @staticmethod
    async def check_access_token(request: Request, token: str = Header(...)) -> User:
        headers = request.headers.mutablecopy()
        headers["auth"] = f"{token}"
        headers["accept"] = "application/json"
        del headers["Content-Length"]

        async with httpx.AsyncClient() as client:
            response = await client.get(
                settings.CHECK_TOKEN_URL,
                headers=headers,
            )
            response = response.json()
            if response.get("status") != ResponseStatus.success:
                raise SuperApiException(
                    status_code=int(response.get('code')),
                    detail=response.get('message'),
                )
        return User(**response.get('data'))

    @staticmethod
    async def refresh_tokens(request: Request, refresh_token: str = Header(...)) -> TokenInfo:
        headers = request.headers.mutablecopy()
        headers["refresh"] = f"{refresh_token}"
        headers["accept"] = "application/json"
        del headers["Content-Length"]

        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.REFRESH_TOKENS_URL,
                headers=headers,
            )
            response = response.json()
            if response.get("status") != ResponseStatus.success:
                raise SuperApiException(
                    status_code=int(response.get('code')),
                    detail=response.get('message'),
                )
        return response.get("data")
