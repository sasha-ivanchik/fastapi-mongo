from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path.cwd().resolve().parent
env_path = BASE_DIR / ".env"


class AuthJWT(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_path, env_file_encoding="utf-8", extra="allow"
    )

    PRIVATE_KEY_PATH: Path = Path.cwd() / "certs" / "jwt-private.pem"
    PUBLIC_KEY_PATH: Path = Path.cwd() / "certs" / "jwt-public.pem"
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_SEC: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    TOKEN_ENCRYPTION_SECRET: str
    TOKEN_ENCRYPTION_SALT: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_path, env_file_encoding="utf-8", extra="allow"
    )
    # postgres settings for auth
    AUTH_DATABASE_URL: str
    AUTH_DB_HOST: str
    AUTH_DB_PORT: int
    AUTH_DB_PASS: str
    AUTH_DB_NAME: str
    AUTH_DB_USER: str
    AUTH_DB_PGUSER: str
    AUTH_JWT: AuthJWT = AuthJWT()


settings = Settings()
