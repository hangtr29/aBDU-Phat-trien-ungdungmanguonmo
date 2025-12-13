from pathlib import Path
from typing import List
from functools import lru_cache
import json
import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, field_validator

# Tìm file .env - thử nhiều vị trí
env_path = None
possible_paths = [
    Path(__file__).resolve().parent.parent / ".env",  # fastapi_app/.env
    Path(__file__).resolve().parent / ".env",  # fastapi_app/core/.env
]

for path in possible_paths:
    if path.exists():
        env_path = path
        break

if not env_path:
    # Nếu không tìm thấy, tạo đường dẫn mặc định
    env_path = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    jwt_alg: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7
    allowed_origins: List[AnyHttpUrl] = []

    @field_validator('allowed_origins', mode='before')
    @classmethod
    def parse_allowed_origins(cls, v):
        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
                return [parsed]
            except json.JSONDecodeError:
                # Nếu không phải JSON, thử split bằng dấu phẩy
                return [url.strip() for url in v.split(',') if url.strip()]
        return v if v else []

    model_config = SettingsConfigDict(
        env_file=str(env_path) if env_path.exists() else None,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Bỏ qua các field không khớp
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()

