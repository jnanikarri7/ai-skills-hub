from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AI DE Hub"
    jwt_secret: str = "CHANGE_ME_IN_ENV"
    jwt_alg: str = "HS256"
    access_token_minutes: int = 60 * 24
    database_url: str = "sqlite:///./aidehub.db"
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:8000"]

settings = Settings()