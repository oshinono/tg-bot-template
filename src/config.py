from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    token: str
    
    redis_url: str
    postgres_url: str


settings = Settings()