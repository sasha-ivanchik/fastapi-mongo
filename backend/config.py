from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path.cwd().resolve().parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8")

    # main mongo db settings
    mongo_host: str
    mongo_port: str
    mongo_url: str
    mongo_user: str
    mongo_pass: str
    mongo_db: str
    mongo_collection: str
    # redis cache settings
    redis_url: str
    redis_db: str
    redis_port: int
    redis_password: str
    cache_time_sec: int
    # celery settings (background tasks)
    celery_broker_url: str
    celery_result_backend: str
    # proxy to auth
    LOGIN_URL: str
    SIGNUP_URL: str
    CHECK_TOKEN_URL: str
    REFRESH_TOKENS_URL: str


settings = Settings()
