from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    MONGODB_URL: str
    DATABASE_NAME: str = "image_search"
    CRAWLER_THREADS: int = 4
    CRAWLER_DEPTH: int = 2
    IMAGE_EXTENSIONS: list = [".jpg", ".jpeg", ".png", ".webp"]
    VECTOR_DIMENSION: int = 512
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()