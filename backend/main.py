import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware

from core.api import router as todo_router

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]

app = FastAPI(middleware=middleware)
app.include_router(todo_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
    )
