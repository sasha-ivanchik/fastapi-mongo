from fastapi import status, Request, Header
import httpx

from utils.exceptions import SuperApiException
from .models import Todo, Token, User, TodoUpdate
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
        document_filter = {"username": user.username}
        db_query = await self.repository.get_list(document_filter)
        todos = [Todo(**document) async for document in db_query] if db_query else []
        return todos

    async def retrieve_document(
            self,
            user: User,
            title: str,
    ) -> Todo:
        document_filter = {"title": title, "username": user.username}
        if document := await self.repository.get(document_filter):
            return document
        else:
            raise SuperApiException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No data",
            )

    async def create_document(
            self,
            user: User,
            document: Todo,
    ) -> Todo:
        try:
            if await self.repository.get(
                    {"title": document.title, "username": user.username}
            ):
                raise SuperApiException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Already exist",
                )

            new_doc_dict = document.model_dump()
            new_doc_dict.update({"username": user.username})

            return await self.repository.create(new_doc_dict)

        except SuperApiException:
            raise

        except Exception:
            raise SuperApiException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong. Retry.",
            )

    async def update_document(
            self,
            user: User,
            update_todo: TodoUpdate,
    ) -> Todo:
        doc_filter = {"title": update_todo.title, "username": user.username}
        doc_setter = update_todo.model_dump(exclude_none=True)
        del doc_setter["title"]

        document = await self.repository.update(doc_filter, doc_setter)
        if document:
            return document

        raise SuperApiException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong. Retry.",
        )

    async def delete_document(
            self,
            user: User,
            title: str,
    ) -> bool:
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
    ) -> Token:
        data = {
            "username": username,
            "password": password,
        }

        headers = request.headers.mutablecopy()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["accept"] = "application/json"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.LOGIN_URL,
                headers=headers,
                data=data,
            )
            response = response.json()

        if not response.get("access_token"):
            raise SuperApiException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Wrong username or password",
            )
        return response

    @staticmethod
    async def signup_user(
            request: Request,
            email: str,
            password: str,
            username: str,
    ) -> Token:
        data = {
            "username": username,
            "password": password,
            "email": email,
        }

        headers = request.headers.mutablecopy()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["accept"] = "application/json"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.SIGNUP_URL,
                headers=headers,
                data=data,
            )
            response = response.json()
            if not response.get("access_token"):
                raise SuperApiException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Retry.",
                )
        return response

    @staticmethod
    async def check_token(request: Request, token: str = Header(...)) -> User:
        headers = request.headers.mutablecopy()
        headers["Authorization"] = f"Bearer {token}"
        headers["accept"] = "application/json"
        del headers["Content-Length"]

        async with httpx.AsyncClient() as client:
            response = await client.get(
                settings.CHECK_TOKEN_URL,
                headers=headers,
            )
            response = response.json()
            if not response.get("username"):
                raise SuperApiException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Wrong username or password",
                )
        return User(**response)
