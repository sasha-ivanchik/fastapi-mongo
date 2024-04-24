import uvicorn
from fastapi import FastAPI

from core.auth.api_auth import router as auth_router
from core.users.api_users import router as users_router

# from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(users_router)
app.include_router(auth_router)

# origins = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173"
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
    )
