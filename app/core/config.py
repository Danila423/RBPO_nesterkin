from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "SecDev Course App"
    VERSION: str = "0.2.0"

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/secdev"
    JWT_SECRET_KEY: str = "CHANGE_ME"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    class Config:
        env_file = ".env"


settings = Settings()
