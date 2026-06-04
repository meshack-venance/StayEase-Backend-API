from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "StayEase API"
    app_version: str = "1.0.0"
    app_debug: bool = True
    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"
    # These can be overridden with UPLOAD_DIR and MAX_UPLOAD_SIZE_MB in .env.
    upload_dir: str = "uploads"
    max_upload_size_mb: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
