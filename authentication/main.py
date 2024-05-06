import uvicorn
from fastapi import FastAPI

from core.auth.api_auth import router as auth_router
# from core.users.api_users import router as users_router
from exceptions_handlers import registered_exception_handlers

app = FastAPI(exception_handlers=registered_exception_handlers)
# app.include_router(users_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
    )
